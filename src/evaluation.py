"""Evaluation module for measuring RAG system performance."""

import logging
import math
import json
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from .retrieval import SemanticRetriever

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EvaluationMetrics:
    """Container for evaluation metrics."""
    precision_at_k: Dict[int, float]
    recall_at_k: Dict[int, float]
    mrr: float
    ndcg_at_k: Dict[int, float]

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)

    def __str__(self) -> str:
        """String representation."""
        lines = ["Evaluation Metrics:"]
        lines.append(f"  MRR: {self.mrr:.4f}")

        lines.append("  Precision@K:")
        for k, p in sorted(self.precision_at_k.items()):
            lines.append(f"    P@{k}: {p:.4f}")

        lines.append("  Recall@K:")
        for k, r in sorted(self.recall_at_k.items()):
            lines.append(f"    R@{k}: {r:.4f}")

        lines.append("  NDCG@K:")
        for k, n in sorted(self.ndcg_at_k.items()):
            lines.append(f"    NDCG@{k}: {n:.4f}")

        return "\n".join(lines)


@dataclass
class QueryResult:
    """Container for a single query's evaluation results."""
    query: str
    retrieved_docs: List[str]
    relevant_docs: Set[str]
    metrics: EvaluationMetrics

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "query": self.query,
            "retrieved_docs": self.retrieved_docs,
            "relevant_docs": list(self.relevant_docs),
            "metrics": self.metrics.to_dict()
        }


class MetricsCalculator:
    """Calculator for information retrieval metrics."""

    @staticmethod
    def precision_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
        """
        Calculate Precision@K.

        Precision@K = (Number of relevant items in top K) / K

        Args:
            retrieved: List of retrieved document IDs in ranked order
            relevant: Set of relevant document IDs (ground truth)
            k: Cutoff position

        Returns:
            Precision@K score (0.0 to 1.0)
        """
        if k <= 0 or not retrieved:
            return 0.0

        retrieved_at_k = retrieved[:k]
        relevant_retrieved = len([doc for doc in retrieved_at_k if doc in relevant])

        return relevant_retrieved / k

    @staticmethod
    def recall_at_k(retrieved: List[str], relevant: Set[str], k: int) -> float:
        """
        Calculate Recall@K.

        Recall@K = (Number of relevant items in top K) / (Total number of relevant items)

        Args:
            retrieved: List of retrieved document IDs in ranked order
            relevant: Set of relevant document IDs (ground truth)
            k: Cutoff position

        Returns:
            Recall@K score (0.0 to 1.0)
        """
        if not relevant or k <= 0 or not retrieved:
            return 0.0

        retrieved_at_k = retrieved[:k]
        relevant_retrieved = len([doc for doc in retrieved_at_k if doc in relevant])

        return relevant_retrieved / len(relevant)

    @staticmethod
    def mean_reciprocal_rank(retrieved: List[str], relevant: Set[str]) -> float:
        """
        Calculate Mean Reciprocal Rank (MRR).

        MRR = 1 / (rank of first relevant item)
        Returns 0 if no relevant items found.

        Args:
            retrieved: List of retrieved document IDs in ranked order
            relevant: Set of relevant document IDs (ground truth)

        Returns:
            MRR score (0.0 to 1.0)
        """
        if not retrieved or not relevant:
            return 0.0

        for rank, doc in enumerate(retrieved, start=1):
            if doc in relevant:
                return 1.0 / rank

        return 0.0

    @staticmethod
    def dcg_at_k(retrieved: List[str], relevant: Set[str], k: int,
                 relevance_scores: Optional[Dict[str, float]] = None) -> float:
        """
        Calculate Discounted Cumulative Gain at K.

        DCG@K = sum(rel_i / log2(i + 1)) for i in 1..K

        Args:
            retrieved: List of retrieved document IDs in ranked order
            relevant: Set of relevant document IDs (ground truth)
            k: Cutoff position
            relevance_scores: Optional dict mapping doc_id to relevance score (default: 1.0 for relevant, 0.0 for not)

        Returns:
            DCG@K score
        """
        if k <= 0 or not retrieved:
            return 0.0

        dcg = 0.0
        for i, doc in enumerate(retrieved[:k], start=1):
            if relevance_scores and doc in relevance_scores:
                rel = relevance_scores[doc]
            else:
                rel = 1.0 if doc in relevant else 0.0

            dcg += rel / math.log2(i + 1)

        return dcg

    @staticmethod
    def ndcg_at_k(retrieved: List[str], relevant: Set[str], k: int,
                  relevance_scores: Optional[Dict[str, float]] = None) -> float:
        """
        Calculate Normalized Discounted Cumulative Gain at K.

        NDCG@K = DCG@K / IDCG@K
        where IDCG@K is the ideal DCG (if all relevant items were ranked first)

        Args:
            retrieved: List of retrieved document IDs in ranked order
            relevant: Set of relevant document IDs (ground truth)
            k: Cutoff position
            relevance_scores: Optional dict mapping doc_id to relevance score

        Returns:
            NDCG@K score (0.0 to 1.0)
        """
        if k <= 0 or not retrieved or not relevant:
            return 0.0

        # Calculate DCG@K
        dcg = MetricsCalculator.dcg_at_k(retrieved, relevant, k, relevance_scores)

        # Calculate IDCG@K (ideal DCG with perfect ranking)
        if relevance_scores:
            # Sort by relevance scores descending
            ideal_ranking = sorted(relevance_scores.items(), key=lambda x: x[1], reverse=True)
            ideal_docs = [doc for doc, _ in ideal_ranking[:k]]
        else:
            # Just put all relevant docs first
            ideal_docs = list(relevant)[:k]

        idcg = MetricsCalculator.dcg_at_k(ideal_docs, relevant, k, relevance_scores)

        if idcg == 0.0:
            return 0.0

        return dcg / idcg


class Evaluator:
    """Evaluator for RAG system performance."""

    def __init__(self, retriever: SemanticRetriever, k_values: List[int] = None,
                 deduplicate: bool = False, min_similarity: float = 0.0):
        """
        Initialize evaluator.

        Args:
            retriever: Retriever instance to evaluate
            k_values: List of K values to evaluate at (default: [1, 3, 5, 10])
            deduplicate: If True, deduplicate results by source document
            min_similarity: Minimum similarity score threshold (0.0 to 1.0)
        """
        self.retriever = retriever
        self.k_values = k_values or [1, 3, 5, 10]
        self.calculator = MetricsCalculator()
        self.deduplicate = deduplicate
        self.min_similarity = min_similarity

    def evaluate_query(self, query: str, relevant_docs: Set[str],
                      k_max: int = 10,
                      relevance_scores: Optional[Dict[str, float]] = None) -> QueryResult:
        """
        Evaluate a single query.

        Args:
            query: Query text
            relevant_docs: Set of relevant document filenames (ground truth)
            k_max: Maximum K value to retrieve
            relevance_scores: Optional relevance scores for graded relevance

        Returns:
            QueryResult with metrics
        """
        # Retrieve documents with optional deduplication
        if self.deduplicate:
            results = self.retriever.retrieve_by_source(query, k=k_max, unique_sources=True)
        else:
            results = self.retriever.retrieve(query, k=k_max)

        # Apply minimum similarity threshold if specified
        if self.min_similarity > 0.0:
            results = [r for r in results if r['similarity_score'] >= self.min_similarity]

        retrieved_docs = [r['source'] for r in results]

        # Calculate metrics at different K values
        precision_at_k = {}
        recall_at_k = {}
        ndcg_at_k = {}

        for k in self.k_values:
            if k <= k_max:
                precision_at_k[k] = self.calculator.precision_at_k(retrieved_docs, relevant_docs, k)
                recall_at_k[k] = self.calculator.recall_at_k(retrieved_docs, relevant_docs, k)
                ndcg_at_k[k] = self.calculator.ndcg_at_k(retrieved_docs, relevant_docs, k, relevance_scores)

        # Calculate MRR
        mrr = self.calculator.mean_reciprocal_rank(retrieved_docs, relevant_docs)

        metrics = EvaluationMetrics(
            precision_at_k=precision_at_k,
            recall_at_k=recall_at_k,
            mrr=mrr,
            ndcg_at_k=ndcg_at_k
        )

        return QueryResult(
            query=query,
            retrieved_docs=retrieved_docs,
            relevant_docs=relevant_docs,
            metrics=metrics
        )

    def evaluate_batch(self, test_queries: List[Dict]) -> Dict:
        """
        Evaluate a batch of queries.

        Args:
            test_queries: List of dicts with 'query' and 'relevant_docs' keys
                         Optional 'relevance_scores' key for graded relevance

        Returns:
            Dictionary with individual and aggregate results
        """
        logger.info(f"Evaluating {len(test_queries)} queries...")

        query_results = []

        for i, test_case in enumerate(test_queries, 1):
            query = test_case['query']
            relevant_docs = set(test_case['relevant_docs'])
            relevance_scores = test_case.get('relevance_scores', None)

            logger.info(f"[{i}/{len(test_queries)}] Evaluating: '{query}'")

            result = self.evaluate_query(query, relevant_docs,
                                        k_max=max(self.k_values),
                                        relevance_scores=relevance_scores)
            query_results.append(result)

        # Calculate aggregate metrics
        aggregate_metrics = self._aggregate_metrics(query_results)

        return {
            "query_results": query_results,
            "aggregate_metrics": aggregate_metrics,
            "num_queries": len(test_queries),
            "k_values": self.k_values
        }

    def _aggregate_metrics(self, query_results: List[QueryResult]) -> EvaluationMetrics:
        """
        Aggregate metrics across multiple queries.

        Args:
            query_results: List of QueryResult objects

        Returns:
            Aggregated EvaluationMetrics (averaged)
        """
        if not query_results:
            return EvaluationMetrics(
                precision_at_k={},
                recall_at_k={},
                mrr=0.0,
                ndcg_at_k={}
            )

        n = len(query_results)

        # Average Precision@K
        precision_at_k = {}
        for k in self.k_values:
            precision_at_k[k] = sum(qr.metrics.precision_at_k.get(k, 0.0) for qr in query_results) / n

        # Average Recall@K
        recall_at_k = {}
        for k in self.k_values:
            recall_at_k[k] = sum(qr.metrics.recall_at_k.get(k, 0.0) for qr in query_results) / n

        # Average NDCG@K
        ndcg_at_k = {}
        for k in self.k_values:
            ndcg_at_k[k] = sum(qr.metrics.ndcg_at_k.get(k, 0.0) for qr in query_results) / n

        # Mean of MRRs
        mrr = sum(qr.metrics.mrr for qr in query_results) / n

        return EvaluationMetrics(
            precision_at_k=precision_at_k,
            recall_at_k=recall_at_k,
            mrr=mrr,
            ndcg_at_k=ndcg_at_k
        )


class EvaluationReporter:
    """Reporter for evaluation results."""

    @staticmethod
    def print_results(evaluation_results: Dict):
        """
        Print evaluation results to console.

        Args:
            evaluation_results: Results from Evaluator.evaluate_batch()
        """
        print("\n" + "=" * 80)
        print("EVALUATION RESULTS")
        print("=" * 80)
        print(f"Number of queries: {evaluation_results['num_queries']}")
        print(f"K values: {evaluation_results['k_values']}")
        print()

        # Aggregate metrics
        print("AGGREGATE METRICS")
        print("-" * 80)
        print(evaluation_results['aggregate_metrics'])
        print()

        # Individual query results
        print("INDIVIDUAL QUERY RESULTS")
        print("-" * 80)
        for i, qr in enumerate(evaluation_results['query_results'], 1):
            print(f"\n[{i}] Query: '{qr.query}'")
            print(f"    Relevant docs: {len(qr.relevant_docs)}")
            print(f"    Retrieved: {qr.retrieved_docs[:5]}")  # Show first 5
            print(f"    Metrics:")
            for k in sorted(qr.metrics.precision_at_k.keys()):
                p = qr.metrics.precision_at_k[k]
                r = qr.metrics.recall_at_k[k]
                n = qr.metrics.ndcg_at_k[k]
                print(f"      @{k}: P={p:.3f}, R={r:.3f}, NDCG={n:.3f}")
            print(f"      MRR: {qr.metrics.mrr:.3f}")

        print("\n" + "=" * 80)

    @staticmethod
    def save_results(evaluation_results: Dict, output_path: Path):
        """
        Save evaluation results to JSON file.

        Args:
            evaluation_results: Results from Evaluator.evaluate_batch()
            output_path: Path to save JSON file
        """
        # Convert QueryResult objects to dicts
        serializable_results = {
            "num_queries": evaluation_results['num_queries'],
            "k_values": evaluation_results['k_values'],
            "aggregate_metrics": evaluation_results['aggregate_metrics'].to_dict(),
            "query_results": [qr.to_dict() for qr in evaluation_results['query_results']],
            "timestamp": datetime.now().isoformat()
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)

        logger.info(f"Evaluation results saved to {output_path}")

    @staticmethod
    def generate_markdown_report(evaluation_results: Dict, output_path: Path):
        """
        Generate a Markdown report of evaluation results.

        Args:
            evaluation_results: Results from Evaluator.evaluate_batch()
            output_path: Path to save markdown file
        """
        lines = []

        lines.append("# RAG System Evaluation Report")
        lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"\n**Number of Queries:** {evaluation_results['num_queries']}")
        lines.append(f"\n**K Values:** {evaluation_results['k_values']}")
        lines.append("\n---\n")

        # Aggregate metrics table
        lines.append("## Aggregate Metrics\n")
        agg = evaluation_results['aggregate_metrics']

        lines.append("### Mean Reciprocal Rank (MRR)")
        lines.append(f"\n**MRR:** {agg.mrr:.4f}\n")

        lines.append("### Precision@K\n")
        lines.append("| K | Precision@K |")
        lines.append("|---|-------------|")
        for k in sorted(agg.precision_at_k.keys()):
            lines.append(f"| {k} | {agg.precision_at_k[k]:.4f} |")

        lines.append("\n### Recall@K\n")
        lines.append("| K | Recall@K |")
        lines.append("|---|----------|")
        for k in sorted(agg.recall_at_k.keys()):
            lines.append(f"| {k} | {agg.recall_at_k[k]:.4f} |")

        lines.append("\n### NDCG@K\n")
        lines.append("| K | NDCG@K |")
        lines.append("|---|--------|")
        for k in sorted(agg.ndcg_at_k.keys()):
            lines.append(f"| {k} | {agg.ndcg_at_k[k]:.4f} |")

        # Individual results
        lines.append("\n---\n")
        lines.append("## Individual Query Results\n")

        for i, qr in enumerate(evaluation_results['query_results'], 1):
            lines.append(f"\n### Query {i}: \"{qr.query}\"\n")
            lines.append(f"- **Relevant Documents:** {len(qr.relevant_docs)}")
            lines.append(f"- **MRR:** {qr.metrics.mrr:.4f}\n")

            lines.append("**Top Retrieved Documents:**")
            for j, doc in enumerate(qr.retrieved_docs[:5], 1):
                relevant_mark = "✓" if doc in qr.relevant_docs else "✗"
                lines.append(f"{j}. {doc} {relevant_mark}")

            lines.append("\n**Metrics:**\n")
            lines.append("| K | Precision | Recall | NDCG |")
            lines.append("|---|-----------|--------|------|")
            for k in sorted(qr.metrics.precision_at_k.keys()):
                p = qr.metrics.precision_at_k[k]
                r = qr.metrics.recall_at_k[k]
                n = qr.metrics.ndcg_at_k[k]
                lines.append(f"| {k} | {p:.4f} | {r:.4f} | {n:.4f} |")

        # Write to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        logger.info(f"Markdown report saved to {output_path}")


def create_sample_test_queries() -> List[Dict]:
    """
    Create sample test queries for demonstration.

    Returns:
        List of test query dictionaries
    """
    # These are examples - you'll need to replace with actual relevant documents
    # based on your dataset
    test_queries = [
        {
            "query": "machine learning algorithms for classification",
            "relevant_docs": {
                # Add actual filenames from your dataset that are relevant
                # Example: "2509.12345v1.pdf", "2509.67890v1.pdf"
            }
        },
        {
            "query": "natural language processing and text analysis",
            "relevant_docs": {
                # Add actual filenames
            }
        },
        {
            "query": "deep learning neural networks",
            "relevant_docs": {
                # Add actual filenames
            }
        }
    ]

    return test_queries


def main():
    """Test evaluation module."""
    base_dir = Path(__file__).parent.parent
    chroma_path = base_dir / "chroma_db"

    # Initialize retriever
    logger.info("Initializing retriever...")
    retriever = SemanticRetriever(str(chroma_path))

    # Create evaluator
    evaluator = Evaluator(retriever, k_values=[1, 3, 5, 10])

    # Example: Test single query evaluation
    logger.info("\n" + "=" * 80)
    logger.info("TESTING SINGLE QUERY EVALUATION")
    logger.info("=" * 80)

    # First, let's retrieve some docs to see what we have
    test_query = "machine learning"
    results = retriever.retrieve(test_query, k=5)

    print(f"\nQuery: '{test_query}'")
    print("Retrieved documents:")
    for i, r in enumerate(results, 1):
        print(f"  {i}. {r['source']} (similarity: {r['similarity_score']:.3f})")

    # Create a test case using the first 2 retrieved docs as "relevant"
    # (This is just for demonstration - in real evaluation you'd have ground truth)
    relevant_docs = {results[0]['source'], results[1]['source']}

    print(f"\nMarking as relevant (for demo): {relevant_docs}")

    # Evaluate
    query_result = evaluator.evaluate_query(test_query, relevant_docs, k_max=10)

    print("\nMetrics:")
    print(query_result.metrics)

    # Example: Batch evaluation
    logger.info("\n" + "=" * 80)
    logger.info("TESTING BATCH EVALUATION")
    logger.info("=" * 80)

    # Create sample test queries
    # You should replace these with actual ground truth
    test_queries = [
        {
            "query": "machine learning",
            "relevant_docs": relevant_docs  # Using demo relevant docs
        },
        {
            "query": "neural networks",
            "relevant_docs": {results[0]['source']}  # Just one relevant doc for demo
        }
    ]

    # Run batch evaluation
    evaluation_results = evaluator.evaluate_batch(test_queries)

    # Print results
    EvaluationReporter.print_results(evaluation_results)

    # Save results
    output_dir = base_dir / "evaluation_results"
    EvaluationReporter.save_results(
        evaluation_results,
        output_dir / "results.json"
    )
    EvaluationReporter.generate_markdown_report(
        evaluation_results,
        output_dir / "report.md"
    )

    logger.info("\nEvaluation complete!")


if __name__ == "__main__":
    main()
