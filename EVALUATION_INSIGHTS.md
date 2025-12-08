# RAG System Evaluation Insights

**Date:** December 8, 2025
**Finding:** Deduplication reveals true performance metrics

---

## Key Discovery

Our original evaluation metrics were **inflated by counting duplicate chunks** from the same source documents. When we deduplicate to measure performance on **unique documents**, we get the true picture of system performance.

---

## Results Comparison

### Baseline (With Duplicate Chunks)
- **MRR:** 0.9375
- **Precision@5:** 0.6000
- **Recall@5:** 1.0625 (>1.0 indicates duplicate counting!)
- **NDCG@5:** 0.9823

### With Deduplication (Unique Documents Only)
- **MRR:** 0.9375 (unchanged - first result usually correct)
- **Precision@5:** 0.4750 (-20.83%)
- **Recall@5:** 0.8333 (-21.57%, now <1.0 as expected)
- **NDCG@5:** Similar (ranking quality maintained)

### With Minimum Similarity Threshold (0.3)
- **Impact:** Minimal (-2.5% change)
- **Reason:** Most results already have similarity > 0.3
- **Conclusion:** Threshold of 0.3 is too low to filter effectively

---

## What This Means

### The Good News
1. **MRR=0.9375 is real** - System excels at finding *a* relevant result at rank 1
2. **Ranking quality is strong** - NDCG shows good ordering
3. **We're finding most relevant docs** - R@5=0.8333 means 83% coverage

### The Reality Check
1. **True Precision@5 is 47.5%**, not 60%
2. **Original metrics overcounted** by treating chunks as separate documents
3. **Deduplication is necessary** for honest evaluation

### Why Deduplication "Hurt" Performance

The seeming decrease isn't actually worse performance - it's **honest measurement**:

**Before (Inflated):**
- Query returns 5 chunks: [DocA-chunk1, DocA-chunk2, DocB-chunk1, DocC-chunk1, DocD-chunk1]
- 4 out of 5 are from relevant docs
- Precision@5 = 4/5 = 0.80
- But we only retrieved 4 UNIQUE documents!

**After (Accurate):**
- Query returns 5 unique docs: [DocA, DocB, DocC, DocD, DocE]
- 3 out of 5 are relevant
- Precision@5 = 3/5 = 0.60
- This is the TRUE precision on unique documents

---

## Interpretation

### Recall > 1.0 Was a Red Flag

```
Baseline Recall@5:  1.0625
Baseline Recall@10: 1.7292
```

**What this means:**
- If there are 3 relevant documents total
- Recall@5 = 1.0625 means we "found" 3.19 documents
- **Impossible!** Can't find more than 100% of relevant docs
- **Cause:** Counting multiple chunks from same document

**After deduplication:**
```
Dedup Recall@5:  0.8333
Dedup Recall@10: 0.8958
```

Now makes sense - we found 83-90% of relevant unique documents.

---

## Recommendations Going Forward

### 1. Use Deduplication for All Future Evaluations ✅
**Reason:** Honest measurement of unique document retrieval
**Implementation:** Always use `deduplicate=True` in Evaluator

### 2. Adjust Performance Expectations
- **Target Precision@5:** 0.60-0.70 on unique docs (not 0.70-0.80)
- **Current Performance:** 0.4750 is below target
- **Gap to close:** +12-22 percentage points

### 3. Focus on Real Improvements
Now that we have honest metrics, we can pursue genuine improvements:

**High Priority:**
- Query expansion (add domain-specific terms)
- Reranking with cross-encoder
- Hybrid search (BM25 + semantic)

**Expected Impact:**
- Query expansion: P@5 from 0.475 → 0.55 (+16%)
- Reranking: P@5 from 0.55 → 0.65 (+18%)
- **Combined: P@5 ≈ 0.65** (meets adjusted target)

### 4. Keep Threshold at 0.3 (or Remove It)
- **Current Impact:** -2.5% (minimal)
- **Reason:** Most similarities already > 0.3
- **Options:**
  - Remove threshold (not helping much)
  - Increase to 0.5 (more aggressive filtering)
  - Keep at 0.3 as safety net

---

## Updated Performance Goals

### Original (Inflated) Goals
- Precision@5 > 0.70
- Recall@10 > 0.80
- Based on chunk-level counting

### Revised (Honest) Goals
- **Precision@5 > 0.60** on unique documents
- **Recall@10 > 0.90** on unique documents
- **MRR > 0.90** (already meeting this!)

### Current Status vs. Revised Goals
| Metric | Goal | Current (Dedup) | Status |
|--------|------|-----------------|--------|
| MRR | > 0.90 | 0.9375 | ✅ EXCEEDS |
| P@5 | > 0.60 | 0.4750 | ❌ BELOW (-20.8%) |
| R@10 | > 0.90 | 0.8958 | ⚠️ CLOSE (-0.5%) |

---

## Lessons Learned

### 1. Evaluation Methodology Matters
- Chunk-level vs. document-level metrics give different pictures
- **Always use document-level** for user-facing metrics
- Chunks are implementation details, users care about unique docs

### 2. Recall > 1.0 Should Trigger Investigation
- Mathematically impossible for recall to exceed 1.0
- Sign of double-counting or evaluation bug
- **Red flag:** Check your evaluation logic

### 3. "Improvements" May Reveal Truth
- Deduplication didn't "hurt" performance
- It revealed the true baseline
- Sometimes apparent regressions are actually better measurement

### 4. Precision-Recall Tradeoff Still Applies
- Deduplication reduces both precision AND recall
- But gives honest picture
- Can now make informed decisions about improvements

---

## Action Items

### Immediate
1. ✅ Document these findings (this file)
2. ✅ Update evaluation to use deduplication by default
3. ⏳ Revise project documentation with honest metrics

### Short-term
4. Implement query expansion
5. Re-evaluate with query expansion
6. Document improvement (if any)

### Medium-term
7. Implement reranking
8. Implement hybrid search
9. Final evaluation before submission

---

## For Project Writeup

**Important points to include:**

1. **Initial Discovery:**
   - "Initial evaluation showed P@5=0.60, but further analysis revealed this was inflated by duplicate chunks"

2. **Methodology Refinement:**
   - "Implemented source-level deduplication to measure performance on unique documents"
   - "This revealed true P@5=0.475, providing honest baseline for improvements"

3. **Learning Moment:**
   - "Recall values >1.0 indicated evaluation methodology issue"
   - "Demonstrates importance of careful metric interpretation"

4. **Honest Assessment:**
   - "System excels at finding A relevant document (MRR=0.9375)"
   - "Room for improvement in precision (P@5=0.475 vs. target 0.60)"
   - "Strong recall (R@10=0.90 finds 90% of relevant docs)"

---

## Conclusion

The deduplication "improvement" actually revealed that our baseline metrics were **measuring the wrong thing**. While this means our system isn't performing as well as we initially thought, it's a valuable learning:

1. **We now have honest metrics** to guide real improvements
2. **We understand the system better** - good at finding relevant docs, but returns duplicates
3. **We have a clear path forward** - query expansion and reranking will genuinely help

**The truth is more valuable than inflated numbers.** We can now pursue real improvements with confidence that our metrics accurately reflect user-facing performance.

---

**Status:** Evaluation methodology refined and documented
**Next:** Implement genuine improvements (query expansion, reranking)
**Due:** December 14, 2025
