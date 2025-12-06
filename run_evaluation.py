"""Run evaluation of the RAG system using test queries."""

import json
import logging
from pathlib import Path
from src.retrieval import SemanticRetriever
from src.evaluation import Evaluator, EvaluationReporter

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def load_test_queries(queries_file: Path) -> list:
    """Load test queries from JSON file."""
    with open(queries_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['test_queries']


def main():
    """Run full evaluation."""
    # Setup paths
    base_dir = Path(__file__).parent
    queries_file = base_dir / "test_queries.json"
    output_dir = base_dir / "evaluation_results"
    chroma_path = base_dir / "chroma_db"
    
    # Load test queries
    logger.info("Loading test queries...")
    test_queries = load_test_queries(queries_file)
    logger.info(f"Loaded {len(test_queries)} test queries\n")
    
    # Initialize retriever
    logger.info("Initializing retriever...")
    retriever = SemanticRetriever(str(chroma_path))
    
    # Create evaluator
    evaluator = Evaluator(retriever, k_values=[1, 3, 5, 10])
    
    # Run evaluation
    logger.info("\n" + "=" * 80)
    logger.info("RUNNING EVALUATION")
    logger.info("=" * 80 + "\n")
    
    evaluation_results = evaluator.evaluate_batch(test_queries)
    
    # Print results
    EvaluationReporter.print_results(evaluation_results)
    
    # Save results
    logger.info("\nSaving results...")
    EvaluationReporter.save_results(
        evaluation_results,
        output_dir / "full_evaluation_results.json"
    )
    EvaluationReporter.generate_markdown_report(
        evaluation_results,
        output_dir / "full_evaluation_report.md"
    )
    
    # Print summary
    print("\n" + "=" * 80)
    print("EVALUATION SUMMARY")
    print("=" * 80)
    agg = evaluation_results['aggregate_metrics']
    print(f"\nMean Reciprocal Rank (MRR): {agg.mrr:.4f}")
    print("\nAverage Metrics:")
    for k in sorted(agg.precision_at_k.keys()):
        p = agg.precision_at_k[k]
        r = agg.recall_at_k[k]
        n = agg.ndcg_at_k[k]
        print(f"  @{k:2d}: Precision={p:.4f}, Recall={r:.4f}, NDCG={n:.4f}")
    
    print("\n" + "=" * 80)
    print("Results saved to:")
    print(f"  - {output_dir / 'full_evaluation_results.json'}")
    print(f"  - {output_dir / 'full_evaluation_report.md'}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
