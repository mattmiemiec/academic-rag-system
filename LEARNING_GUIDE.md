# RAG System Learning Guide

## What We Just Did Today

### Step 1: Text Extraction from PDFs

**The Goal:** Convert 75 PDF files into readable text that we can process.

**What Happened:**
- We created a Python script (`src/data_processing.py`) that:
  1. Opens each PDF file one by one
  2. Extracts all the text from every page
  3. Breaks the text into manageable chunks (512 words each with 50-word overlap)
  4. Saves each PDF's chunks as a JSON file
  5. Creates a metadata CSV file tracking all documents

**Why We Do This:**
- PDFs are formatted for human reading, not for computers to analyze
- Large texts don't fit well in machine learning models - chunking breaks them into pieces
- The overlap between chunks (50 words) helps maintain context so related information doesn't split awkwardly

**Results:**
- All 75 PDFs processed successfully
- Created 1,315 total chunks (some PDFs had more content than others)
- Each chunk is about 512 words (roughly 2 pages of content)

**Technical Details:**
- Handled Unicode encoding issues gracefully (some PDFs had corrupted characters)
- Used PyPDF2 library to read PDF files
- Stored results in `data/processed/` directory as individual JSON files

---

## What Comes Next (Tomorrow)

### Step 2: Generate Embeddings
**What it is:** Convert text chunks into numbers that represent meaning.
- Each chunk will become a list of 384 numbers (called an embedding)
- These numbers capture the "semantic meaning" - so similar texts get similar numbers
- We'll use the `all-MiniLM-L6-v2` model (lightweight but effective)

**Why it matters:** Machine learning models understand numbers, not text. Embeddings are like a "fingerprint" of meaning.

### Step 3: Store in Vector Database (Chroma)
**What it is:** Save all the embeddings in an organized database.
- Think of it like a library catalog, but for text meanings
- Allows fast searching for similar documents

### Step 4: Implement Retrieval (Semantic Search)
**What it is:** When you ask a question, find the most relevant text chunks.
- Compare your question's embedding to all chunk embeddings
- Return the top 5-10 most similar chunks

### Step 5: LLM Integration
**What it is:** Use your local LLM (Mixtral) to generate explanations.
- Feed it the relevant chunks + your question
- It generates why those chunks are relevant

### Step 6: Evaluation Metrics
**What it is:** Measure how good your system is.
- Precision@5: Of top 5 results, how many are actually relevant?
- Recall@10: Of all relevant documents, how many did we find in top 10?
- Other metrics: MRR, NDCG

---

## Key Concepts to Understand

### Chunking
- Breaking large documents into smaller pieces
- Trade-off: Smaller chunks = faster retrieval but might lose context
- Larger chunks = more context but retrieval is slower

### Embeddings
- Turn words/text into vectors (lists of numbers)
- `all-MiniLM-L6-v2` creates 384-dimensional vectors
- Similar meanings = similar numbers = close in vector space

### Vector Database
- Optimized for storing and searching embeddings
- Can find similar items very quickly (using nearest neighbor search)
- We're using Chroma (lightweight, good for local development)

### RAG Architecture
```
User Question
    ↓
Generate Question Embedding
    ↓
Search Vector Database for Similar Chunks
    ↓
Get Top-K Most Similar Chunks
    ↓
Feed Question + Chunks to LLM
    ↓
LLM Generates Explanation
    ↓
User Gets Answer with Sources
```

---

## Files Created Today

| File | Purpose |
|------|---------|
| `src/data_processing.py` | Extracts text from PDFs and creates chunks |
| `data/processed/*_chunks.json` | Individual chunk data for each PDF |
| `data/processed/metadata.csv` | Summary of all documents and chunk counts |

---

## Next Steps (For Tomorrow)

1. Create embedding generation module (`src/embeddings.py`)
2. Run embeddings on all 1,315 chunks
3. Store embeddings in Chroma vector database
4. Test retrieval with sample queries
5. Move toward LLM integration

---

## Questions to Ask Yourself

- Why do we chunk text? What happens if we don't?
- Why do we need embeddings? Why not just search for keywords?
- How does semantic search differ from keyword search?
- Why is the vector database faster than checking all documents?

These are the conceptual foundations that will make everything else make sense.

---

## Quick Reference

**All-MiniLM-L6-v2 Model:**
- Lightweight (22MB)
- Fast inference
- 384-dimensional embeddings
- Good for academic text
- Optimized for semantic similarity

**Your Current Dataset:**
- 75 academic papers
- 1,315 text chunks total
- Stored in: `/Users/matt/Local/academic_rag_system/data/processed/`
