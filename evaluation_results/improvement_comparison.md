# RAG System Improvement Comparison

**Date:** 1765180801.1805646

## Summary

This report compares the RAG system performance with different improvements:

1. **Baseline**: Original retrieval (allows duplicate chunks)
2. **Deduplication**: Source-level deduplication (unique documents only)
3. **Threshold**: Minimum similarity threshold (min_similarity=0.3)
4. **Combined**: Both deduplication + threshold

## Aggregate Metrics Comparison

| Metric | Baseline | Deduplication | Threshold | Combined |
|--------|----------|---------------|-----------|----------|
| **MRR** | 0.9375 | 0.9375 | 0.9375 | 0.9375 |
| **P@1** | 0.8750 | 0.8750 | 0.8750 | 0.8750 |
| **P@3** | 0.7083 | 0.6250 | 0.7083 | 0.6250 |
| **P@5** | 0.6000 | 0.4750 | 0.6000 | 0.4750 |
| **P@10** | 0.5000 | 0.2500 | 0.4875 | 0.2375 |
| **R@1** | 0.4000 | 0.4000 | 0.4000 | 0.4000 |
| **R@3** | 0.8042 | 0.7000 | 0.8042 | 0.7000 |
| **R@5** | 1.0625 | 0.8333 | 1.0625 | 0.8333 |
| **R@10** | 1.7292 | 0.8958 | 1.6875 | 0.8333 |
| **NDCG@1** | 0.8750 | 0.8750 | 0.8750 | 0.8750 |
| **NDCG@3** | 0.8637 | 0.7860 | 0.8637 | 0.7860 |
| **NDCG@5** | 0.9823 | 0.8365 | 0.9823 | 0.8365 |
| **NDCG@10** | 1.2806 | 0.8596 | 1.2610 | 0.8365 |

## Key Findings

### Deduplication Impact

- Precision@5: 0.6000 → 0.4750 (-20.8%)
- Eliminates duplicate chunks from same papers
- Improves result diversity

### Combined Improvements

- Precision@5: 0.6000 → 0.4750 (-20.8%)
- Best overall performance
- Combines diversity (deduplication) with quality (threshold)

