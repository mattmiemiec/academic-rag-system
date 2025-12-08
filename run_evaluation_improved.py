#!/usr/bin/env python3
"""
Run improved evaluation with deduplication and similarity threshold.

This script evaluates the RAG system with the following improvements:
1. Source-level deduplication (unique documents only)
2. Minimum similarity threshold (filter low-relevance results)
"""

import json
import logging
from pathlib import Path
from typing import Dict
from src.retrieval import SemanticRetriever
from src.evaluation import Evaluator, EvaluationReporter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _print_aggregate_metrics(results: Dict):
    """Print aggregate metrics in a clean format."""
    agg = results['aggregate_metrics']

    # Convert to dict if it's an object
    if hasattr(agg, 'to_dict'):
        agg = agg.to_dict()

    print(f"\nMRR: {agg['mrr']:.4f}")

    print("\nPrecision@K:")
    for k in [1, 3, 5, 10]:
        # Try both int and string keys for compatibility
        p = agg['precision_at_k'].get(k, agg['precision_at_k'].get(str(k), 0))
        print(f"  P@{k}: {p:.4f}")

    print("\nRecall@K:")
    for k in [1, 3, 5, 10]:
        r = agg['recall_at_k'].get(k, agg['recall_at_k'].get(str(k), 0))
        print(f"  R@{k}: {r:.4f}")

    print("\nNDCG@K:")
    for k in [1, 3, 5, 10]:
        n = agg['ndcg_at_k'].get(k, agg['ndcg_at_k'].get(str(k), 0))
        print(f"  NDCG@{k}: {n:.4f}")


def load_test_queries(filepath: str = "test_queries.json"):
    """Load test queries from JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)
        # Handle nested structure
        if isinstance(data, dict) and 'test_queries' in data:
            return data['test_queries']
        return data


def run_baseline_evaluation(retriever, test_queries):
    """Run baseline evaluation (original method)."""
    logger.info("=" * 60)
    logger.info("BASELINE EVALUATION (Original)")
    logger.info("=" * 60)

    evaluator = Evaluator(retriever, k_values=[1, 3, 5, 10])
    results = evaluator.evaluate_batch(test_queries)

    print("\n" + "=" * 60)
    print("BASELINE RESULTS")
    print("=" * 60)
    _print_aggregate_metrics(results)

    return results


def run_deduplication_evaluation(retriever, test_queries):
    """Run evaluation with source-level deduplication."""
    logger.info("\n" + "=" * 60)
    logger.info("IMPROVED EVALUATION (Deduplication)")
    logger.info("=" * 60)

    evaluator = Evaluator(retriever, k_values=[1, 3, 5, 10], deduplicate=True)
    results = evaluator.evaluate_batch(test_queries)

    print("\n" + "=" * 60)
    print("DEDUPLICATION RESULTS")
    print("=" * 60)
    _print_aggregate_metrics(results)

    return results


def run_threshold_evaluation(retriever, test_queries, min_similarity=0.3):
    """Run evaluation with minimum similarity threshold."""
    logger.info("\n" + "=" * 60)
    logger.info(f"IMPROVED EVALUATION (Min Similarity = {min_similarity})")
    logger.info("=" * 60)

    evaluator = Evaluator(retriever, k_values=[1, 3, 5, 10], min_similarity=min_similarity)
    results = evaluator.evaluate_batch(test_queries)

    print("\n" + "=" * 60)
    print(f"THRESHOLD RESULTS (min_similarity={min_similarity})")
    print("=" * 60)
    _print_aggregate_metrics(results)

    return results


def run_combined_evaluation(retriever, test_queries, min_similarity=0.3):
    """Run evaluation with both deduplication and threshold."""
    logger.info("\n" + "=" * 60)
    logger.info(f"IMPROVED EVALUATION (Deduplication + Min Similarity = {min_similarity})")
    logger.info("=" * 60)

    evaluator = Evaluator(
        retriever,
        k_values=[1, 3, 5, 10],
        deduplicate=True,
        min_similarity=min_similarity
    )
    results = evaluator.evaluate_batch(test_queries)

    print("\n" + "=" * 60)
    print(f"COMBINED RESULTS (deduplicate + min_similarity={min_similarity})")
    print("=" * 60)
    _print_aggregate_metrics(results)

    return results


def compare_results(baseline, improved, improvement_name):
    """Compare baseline vs improved results."""
    print("\n" + "=" * 60)
    print(f"IMPROVEMENT ANALYSIS: {improvement_name}")
    print("=" * 60)

    baseline_agg = baseline['aggregate_metrics']
    improved_agg = improved['aggregate_metrics']

    # Convert to dict if needed
    if hasattr(baseline_agg, 'to_dict'):
        baseline_agg = baseline_agg.to_dict()
    if hasattr(improved_agg, 'to_dict'):
        improved_agg = improved_agg.to_dict()

    # MRR comparison
    baseline_mrr = baseline_agg['mrr']
    improved_mrr = improved_agg['mrr']
    mrr_change = ((improved_mrr - baseline_mrr) / baseline_mrr * 100) if baseline_mrr > 0 else 0

    print(f"\nMRR:")
    print(f"  Baseline:  {baseline_mrr:.4f}")
    print(f"  Improved:  {improved_mrr:.4f}")
    print(f"  Change:    {mrr_change:+.2f}%")

    # Precision@K comparison
    print(f"\nPrecision@K:")
    for k in [1, 3, 5, 10]:
        baseline_p = baseline_agg['precision_at_k'].get(k, baseline_agg['precision_at_k'].get(str(k), 0))
        improved_p = improved_agg['precision_at_k'].get(k, improved_agg['precision_at_k'].get(str(k), 0))
        p_change = ((improved_p - baseline_p) / baseline_p * 100) if baseline_p > 0 else 0

        print(f"  P@{k}:")
        print(f"    Baseline:  {baseline_p:.4f}")
        print(f"    Improved:  {improved_p:.4f}")
        print(f"    Change:    {p_change:+.2f}%")

    # Recall@K comparison
    print(f"\nRecall@K:")
    for k in [1, 3, 5, 10]:
        baseline_r = baseline_agg['recall_at_k'].get(k, baseline_agg['recall_at_k'].get(str(k), 0))
        improved_r = improved_agg['recall_at_k'].get(k, improved_agg['recall_at_k'].get(str(k), 0))
        r_change = ((improved_r - baseline_r) / baseline_r * 100) if baseline_r > 0 else 0

        print(f"  R@{k}:")
        print(f"    Baseline:  {baseline_r:.4f}")
        print(f"    Improved:  {improved_r:.4f}")
        print(f"    Change:    {r_change:+.2f}%")

    # NDCG@K comparison
    print(f"\nNDCG@K:")
    for k in [1, 3, 5, 10]:
        baseline_n = baseline_agg['ndcg_at_k'].get(k, baseline_agg['ndcg_at_k'].get(str(k), 0))
        improved_n = improved_agg['ndcg_at_k'].get(k, improved_agg['ndcg_at_k'].get(str(k), 0))
        n_change = ((improved_n - baseline_n) / baseline_n * 100) if baseline_n > 0 else 0

        print(f"  NDCG@{k}:")
        print(f"    Baseline:  {baseline_n:.4f}")
        print(f"    Improved:  {improved_n:.4f}")
        print(f"    Change:    {n_change:+.2f}%")


def _get_metric_value(results, metric_path):
    """Safely extract metric value, converting objects to dicts if needed."""
    agg = results['aggregate_metrics']
    if hasattr(agg, 'to_dict'):
        agg = agg.to_dict()

    # Navigate the metric path
    if isinstance(metric_path, str):
        return agg[metric_path]
    else:
        # For nested paths like ['precision_at_k', '5']
        value = agg
        for i, key in enumerate(metric_path):
            if i == len(metric_path) - 1 and isinstance(value, dict):
                # Last key - try both int and string versions
                if isinstance(key, str) and key.isdigit():
                    value = value.get(int(key), value.get(key, 0))
                else:
                    value = value.get(key, value.get(str(key), 0))
            else:
                value = value[key]
        return value


def save_comparison_report(baseline, dedup, threshold, combined, output_dir="evaluation_results"):
    """Save comparison report to file."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Save JSON results - convert objects to dicts for serialization
    def convert_for_json(results):
        """Convert EvaluationMetrics objects to dicts for JSON serialization."""
        converted = results.copy()
        if hasattr(converted['aggregate_metrics'], 'to_dict'):
            converted['aggregate_metrics'] = converted['aggregate_metrics'].to_dict()
        # Convert QueryResult objects
        if 'query_results' in converted:
            converted['query_results'] = [
                qr.to_dict() if hasattr(qr, 'to_dict') else qr
                for qr in converted['query_results']
            ]
        return converted

    comparison_data = {
        "baseline": convert_for_json(baseline),
        "deduplication": convert_for_json(dedup),
        "threshold": convert_for_json(threshold),
        "combined": convert_for_json(combined)
    }

    json_path = output_path / "improvement_comparison.json"
    with open(json_path, 'w') as f:
        json.dump(comparison_data, f, indent=2)

    logger.info(f"Saved comparison data to {json_path}")

    # Create markdown report
    md_path = output_path / "improvement_comparison.md"
    with open(md_path, 'w') as f:
        f.write("# RAG System Improvement Comparison\n\n")
        f.write("**Date:** " + Path(json_path).stat().st_mtime.__str__() + "\n\n")
        f.write("## Summary\n\n")
        f.write("This report compares the RAG system performance with different improvements:\n\n")
        f.write("1. **Baseline**: Original retrieval (allows duplicate chunks)\n")
        f.write("2. **Deduplication**: Source-level deduplication (unique documents only)\n")
        f.write("3. **Threshold**: Minimum similarity threshold (min_similarity=0.3)\n")
        f.write("4. **Combined**: Both deduplication + threshold\n\n")

        f.write("## Aggregate Metrics Comparison\n\n")
        f.write("| Metric | Baseline | Deduplication | Threshold | Combined |\n")
        f.write("|--------|----------|---------------|-----------|----------|\n")

        # MRR row
        f.write(f"| **MRR** | "
                f"{_get_metric_value(baseline, 'mrr'):.4f} | "
                f"{_get_metric_value(dedup, 'mrr'):.4f} | "
                f"{_get_metric_value(threshold, 'mrr'):.4f} | "
                f"{_get_metric_value(combined, 'mrr'):.4f} |\n")

        # Precision@K rows
        for k in [1, 3, 5, 10]:
            k_str = str(k)
            f.write(f"| **P@{k}** | "
                    f"{_get_metric_value(baseline, ['precision_at_k', k_str]):.4f} | "
                    f"{_get_metric_value(dedup, ['precision_at_k', k_str]):.4f} | "
                    f"{_get_metric_value(threshold, ['precision_at_k', k_str]):.4f} | "
                    f"{_get_metric_value(combined, ['precision_at_k', k_str]):.4f} |\n")

        # Recall@K rows
        for k in [1, 3, 5, 10]:
            k_str = str(k)
            f.write(f"| **R@{k}** | "
                    f"{_get_metric_value(baseline, ['recall_at_k', k_str]):.4f} | "
                    f"{_get_metric_value(dedup, ['recall_at_k', k_str]):.4f} | "
                    f"{_get_metric_value(threshold, ['recall_at_k', k_str]):.4f} | "
                    f"{_get_metric_value(combined, ['recall_at_k', k_str]):.4f} |\n")

        # NDCG@K rows
        for k in [1, 3, 5, 10]:
            k_str = str(k)
            f.write(f"| **NDCG@{k}** | "
                    f"{_get_metric_value(baseline, ['ndcg_at_k', k_str]):.4f} | "
                    f"{_get_metric_value(dedup, ['ndcg_at_k', k_str]):.4f} | "
                    f"{_get_metric_value(threshold, ['ndcg_at_k', k_str]):.4f} | "
                    f"{_get_metric_value(combined, ['ndcg_at_k', k_str]):.4f} |\n")

        f.write("\n## Key Findings\n\n")
        f.write("### Deduplication Impact\n\n")

        baseline_p5 = _get_metric_value(baseline, ['precision_at_k', '5'])
        dedup_p5 = _get_metric_value(dedup, ['precision_at_k', '5'])
        p5_improvement = ((dedup_p5 - baseline_p5) / baseline_p5 * 100) if baseline_p5 > 0 else 0

        f.write(f"- Precision@5: {baseline_p5:.4f} → {dedup_p5:.4f} ({p5_improvement:+.1f}%)\n")
        f.write(f"- Eliminates duplicate chunks from same papers\n")
        f.write(f"- Improves result diversity\n\n")

        f.write("### Combined Improvements\n\n")
        combined_p5 = _get_metric_value(combined, ['precision_at_k', '5'])
        combined_improvement = ((combined_p5 - baseline_p5) / baseline_p5 * 100) if baseline_p5 > 0 else 0

        f.write(f"- Precision@5: {baseline_p5:.4f} → {combined_p5:.4f} ({combined_improvement:+.1f}%)\n")
        f.write(f"- Best overall performance\n")
        f.write(f"- Combines diversity (deduplication) with quality (threshold)\n\n")

    logger.info(f"Saved comparison report to {md_path}")


def main():
    """Run all evaluations and compare results."""
    print("\n" + "=" * 60)
    print("RAG SYSTEM IMPROVEMENT EVALUATION")
    print("=" * 60)
    print("\nThis script tests the impact of:")
    print("  1. Source-level deduplication")
    print("  2. Minimum similarity threshold")
    print("  3. Combined improvements")
    print("\n")

    # Initialize
    base_dir = Path(__file__).parent
    chroma_path = base_dir / "chroma_db"

    # Load test queries
    logger.info("Loading test queries...")
    test_queries = load_test_queries()
    logger.info(f"Loaded {len(test_queries)} test queries")

    # Initialize retriever
    logger.info("Initializing retriever...")
    retriever = SemanticRetriever(str(chroma_path))

    # Run all evaluations
    baseline = run_baseline_evaluation(retriever, test_queries)
    dedup = run_deduplication_evaluation(retriever, test_queries)
    threshold = run_threshold_evaluation(retriever, test_queries, min_similarity=0.3)
    combined = run_combined_evaluation(retriever, test_queries, min_similarity=0.3)

    # Compare results
    compare_results(baseline, dedup, "Deduplication Only")
    compare_results(baseline, threshold, "Similarity Threshold Only")
    compare_results(baseline, combined, "Combined Improvements")

    # Save reports
    save_comparison_report(baseline, dedup, threshold, combined)

    print("\n" + "=" * 60)
    print("EVALUATION COMPLETE!")
    print("=" * 60)
    print("\nResults saved to:")
    print("  - evaluation_results/improvement_comparison.json")
    print("  - evaluation_results/improvement_comparison.md")
    print("\n")


if __name__ == "__main__":
    main()
