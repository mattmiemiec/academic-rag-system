# RAG System Evaluation Report

**Generated:** 2025-12-06 16:15:11

**Number of Queries:** 2

**K Values:** [1, 3, 5, 10]

---

## Aggregate Metrics

### Mean Reciprocal Rank (MRR)

**MRR:** 0.5000

### Precision@K

| K | Precision@K |
|---|-------------|
| 1 | 0.5000 |
| 3 | 0.5000 |
| 5 | 0.5000 |
| 10 | 0.2500 |

### Recall@K

| K | Recall@K |
|---|----------|
| 1 | 0.2500 |
| 3 | 0.7500 |
| 5 | 1.2500 |
| 10 | 1.2500 |

### NDCG@K

| K | NDCG@K |
|---|--------|
| 1 | 0.5000 |
| 3 | 0.6533 |
| 5 | 0.9039 |
| 10 | 0.9039 |

---

## Individual Query Results


### Query 1: "machine learning"

- **Relevant Documents:** 2
- **MRR:** 1.0000

**Top Retrieved Documents:**
1. 2509.23577v1.pdf ✓
2. 2509.13388v2.pdf ✓
3. 2509.23577v1.pdf ✓
4. 2509.23577v1.pdf ✓
5. 2509.23577v1.pdf ✓

**Metrics:**

| K | Precision | Recall | NDCG |
|---|-----------|--------|------|
| 1 | 1.0000 | 0.5000 | 1.0000 |
| 3 | 1.0000 | 1.5000 | 1.3066 |
| 5 | 1.0000 | 2.5000 | 1.8078 |
| 10 | 0.5000 | 2.5000 | 1.8078 |

### Query 2: "neural networks"

- **Relevant Documents:** 1
- **MRR:** 0.0000

**Top Retrieved Documents:**
1. 2509.13388v2.pdf ✗
2. 2509.07123v1.pdf ✗
3. 2509.08418v1.pdf ✗
4. 2509.08418v1.pdf ✗
5. 2509.00056v2.pdf ✗

**Metrics:**

| K | Precision | Recall | NDCG |
|---|-----------|--------|------|
| 1 | 0.0000 | 0.0000 | 0.0000 |
| 3 | 0.0000 | 0.0000 | 0.0000 |
| 5 | 0.0000 | 0.0000 | 0.0000 |
| 10 | 0.0000 | 0.0000 | 0.0000 |