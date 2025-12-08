# RAG System Evaluation Report

**Generated:** 2025-12-08 16:58:34

**Number of Queries:** 8

**K Values:** [1, 3, 5, 10]

---

## Aggregate Metrics

### Mean Reciprocal Rank (MRR)

**MRR:** 0.9375

### Precision@K

| K | Precision@K |
|---|-------------|
| 1 | 0.8750 |
| 3 | 0.7083 |
| 5 | 0.6000 |
| 10 | 0.5000 |

### Recall@K

| K | Recall@K |
|---|----------|
| 1 | 0.4000 |
| 3 | 0.8042 |
| 5 | 1.0625 |
| 10 | 1.7292 |

### NDCG@K

| K | NDCG@K |
|---|--------|
| 1 | 0.8750 |
| 3 | 0.8637 |
| 5 | 0.9823 |
| 10 | 1.2806 |

---

## Individual Query Results


### Query 1: "graph neural networks for node classification"

- **Relevant Documents:** 3
- **MRR:** 1.0000

**Top Retrieved Documents:**
1. 2509.07123v1.pdf ✓
2. 2509.07123v1.pdf ✓
3. 2509.08418v1.pdf ✓
4. 2509.08418v1.pdf ✓
5. 2509.07123v1.pdf ✓

**Metrics:**

| K | Precision | Recall | NDCG |
|---|-----------|--------|------|
| 1 | 1.0000 | 0.3333 | 1.0000 |
| 3 | 1.0000 | 1.0000 | 1.0000 |
| 5 | 1.0000 | 1.6667 | 1.3836 |
| 10 | 0.9000 | 3.0000 | 1.9909 |

### Query 2: "medical image segmentation using deep learning"

- **Relevant Documents:** 3
- **MRR:** 1.0000

**Top Retrieved Documents:**
1. 2509.23672v1.pdf ✓
2. 2509.11752v1.pdf ✓
3. 2509.11752v1.pdf ✓
4. 2509.11752v1.pdf ✓
5. 2509.11752v1.pdf ✓

**Metrics:**

| K | Precision | Recall | NDCG |
|---|-----------|--------|------|
| 1 | 1.0000 | 0.3333 | 1.0000 |
| 3 | 1.0000 | 1.0000 | 1.0000 |
| 5 | 1.0000 | 1.6667 | 1.3836 |
| 10 | 0.9000 | 3.0000 | 1.9650 |

### Query 3: "natural language processing with transformers"

- **Relevant Documents:** 5
- **MRR:** 1.0000

**Top Retrieved Documents:**
1. 2509.08438v1.pdf ✓
2. 2509.24294v1.pdf ✓
3. 2509.08438v1.pdf ✓
4. 2509.03972v1.pdf ✓
5. 2509.20617v1.pdf ✓

**Metrics:**

| K | Precision | Recall | NDCG |
|---|-----------|--------|------|
| 1 | 1.0000 | 0.2000 | 1.0000 |
| 3 | 1.0000 | 0.6000 | 1.0000 |
| 5 | 1.0000 | 1.0000 | 1.0000 |
| 10 | 1.0000 | 2.0000 | 1.5410 |

### Query 4: "deep learning optimization algorithms"

- **Relevant Documents:** 2
- **MRR:** 1.0000

**Top Retrieved Documents:**
1. 2509.21653v1.pdf ✓
2. 2509.00045v1.pdf ✗
3. 2509.03378v3.pdf ✗
4. 2509.08438v1.pdf ✗
5. 2509.13388v2.pdf ✗

**Metrics:**

| K | Precision | Recall | NDCG |
|---|-----------|--------|------|
| 1 | 1.0000 | 0.5000 | 1.0000 |
| 3 | 0.3333 | 0.5000 | 0.6131 |
| 5 | 0.2000 | 0.5000 | 0.6131 |
| 10 | 0.1000 | 0.5000 | 0.6131 |

### Query 5: "computer vision object detection"

- **Relevant Documents:** 3
- **MRR:** 0.5000

**Top Retrieved Documents:**
1. 2509.23741v1.pdf ✗
2. 2509.13388v2.pdf ✓
3. 2509.23741v1.pdf ✗
4. 2509.24361v1.pdf ✗
5. 2509.00056v2.pdf ✓

**Metrics:**

| K | Precision | Recall | NDCG |
|---|-----------|--------|------|
| 1 | 0.0000 | 0.0000 | 0.0000 |
| 3 | 0.3333 | 0.3333 | 0.2961 |
| 5 | 0.4000 | 0.6667 | 0.4776 |
| 10 | 0.3000 | 1.0000 | 0.6448 |

### Query 6: "reinforcement learning and decision making"

- **Relevant Documents:** 1
- **MRR:** 1.0000

**Top Retrieved Documents:**
1. 2509.07150v1.pdf ✓
2. 2509.07123v1.pdf ✗
3. 2509.25958v1.pdf ✗
4. 2509.25958v1.pdf ✗
5. 2509.25958v1.pdf ✗

**Metrics:**

| K | Precision | Recall | NDCG |
|---|-----------|--------|------|
| 1 | 1.0000 | 1.0000 | 1.0000 |
| 3 | 0.3333 | 1.0000 | 1.0000 |
| 5 | 0.2000 | 1.0000 | 1.0000 |
| 10 | 0.2000 | 2.0000 | 1.3333 |

### Query 7: "recommendation systems and collaborative filtering"

- **Relevant Documents:** 3
- **MRR:** 1.0000

**Top Retrieved Documents:**
1. 2509.01514v1.pdf ✓
2. 2509.08736v1.pdf ✓
3. 2509.07123v1.pdf ✓
4. 2509.11633v1.pdf ✗
5. 2509.03937v1.pdf ✗

**Metrics:**

| K | Precision | Recall | NDCG |
|---|-----------|--------|------|
| 1 | 1.0000 | 0.3333 | 1.0000 |
| 3 | 1.0000 | 1.0000 | 1.0000 |
| 5 | 0.6000 | 1.0000 | 1.0000 |
| 10 | 0.4000 | 1.3333 | 1.1564 |

### Query 8: "cybersecurity threat detection"

- **Relevant Documents:** 2
- **MRR:** 1.0000

**Top Retrieved Documents:**
1. 2509.11633v1.pdf ✓
2. 2509.11633v1.pdf ✓
3. 2509.04060v1.pdf ✗
4. 2509.23741v1.pdf ✗
5. 2509.23741v1.pdf ✗

**Metrics:**

| K | Precision | Recall | NDCG |
|---|-----------|--------|------|
| 1 | 1.0000 | 0.5000 | 1.0000 |
| 3 | 0.6667 | 1.0000 | 1.0000 |
| 5 | 0.4000 | 1.0000 | 1.0000 |
| 10 | 0.2000 | 1.0000 | 1.0000 |