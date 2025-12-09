# Example CLI Session

This document shows a real example session using the interactive CLI.

---

## Starting the CLI

```bash
cd ~/Local/academic_rag_system
source venv/bin/activate
python rag_cli.py
```

**Output:**
```
╔══════════════════════════════════════════════════════════════════╗
║          Academic RAG System - Interactive CLI                   ║
║                                                                  ║
║  Query 75 academic papers using semantic search and AI          ║
║  Model: Mixtral 8x7b | Embeddings: all-MiniLM-L6-v2            ║
╚══════════════════════════════════════════════════════════════════╝

Available Commands:
  query <text>    - Search for papers (or just type your query)
  mode <type>     - Set generation mode: 'detailed' or 'simple'
  format <type>   - Set output format: 'text', 'json', 'markdown', 'summary'
  results <n>     - Set number of results to retrieve (default: 5)
  history         - Show query history
  save <file>     - Save last result to file
  help            - Show this help message
  clear           - Clear screen
  exit/quit       - Exit the program

Examples:
  > neural networks for image classification
  > mode simple
  > format json
  > results 10

❯
```

---

## Example 1: Basic Query

**User Input:**
```
❯ machine learning for classification
```

**System Response:**
```
Loading RAG system: [████████████████████████████████████████] 100/100 (100.0%)
✓ RAG system initialized


================================================================================
SEARCH QUERY
================================================================================
Query: machine learning for classification
Time: 2025-12-09 15:30:45

Retrieving documents: [████████████████████████████████████████] 100/100 (100.0%)

RETRIEVAL STATISTICS
--------------------------------------------------------------------------------
✓ Retrieved: 5 chunks from 4 unique papers
✓ Average Similarity: 0.412
✓ Retrieval Time: 189.34ms

Generating explanation: [████████████████████████████████████████] 100/100 (100.0%)


================================================================================
SEARCH QUERY
================================================================================
Query: machine learning for classification
Time: 2025-12-09 15:30:45

RETRIEVAL STATISTICS
--------------------------------------------------------------------------------
✓ Retrieved: 5 chunks from 4 unique papers
✓ Average Similarity: 0.412
✓ Retrieval Time: 189.34ms

RETRIEVED DOCUMENTS (5)
--------------------------------------------------------------------------------

[1] 2509.12345v1.pdf
    Similarity: 0.521 ✓
    Excerpt: This paper presents a novel machine learning approach for multi-class
    classification using ensemble methods. The proposed framework combines random
    forests with gradient boosting...

[2] 2509.23456v1.pdf
    Similarity: 0.456 ✓
    Excerpt: We introduce a deep learning architecture for image classification that
    achieves state-of-the-art results on benchmark datasets. The model uses
    convolutional layers...

[3] 2509.34567v1.pdf
    Similarity: 0.389
    Excerpt: Classification of medical images using transfer learning techniques.
    Pre-trained models are fine-tuned on domain-specific datasets...

[4] 2509.45678v1.pdf
    Similarity: 0.378
    Excerpt: This work explores feature selection methods for improving classification
    accuracy. We compare various techniques including PCA, LDA...

[5] 2509.12345v1.pdf
    Similarity: 0.312
    Excerpt: The ensemble approach demonstrates robust performance across multiple
    classification tasks with different data characteristics...

RELEVANCE ANALYSIS
--------------------------------------------------------------------------------
The retrieved papers are highly relevant to machine learning for classification.
Paper [1] directly addresses multi-class classification using ensemble methods,
which are fundamental machine learning techniques. The combination of random
forests and gradient boosting represents a sophisticated approach to improving
classification accuracy.

Paper [2] focuses on deep learning for image classification, demonstrating the
application of neural networks to classification tasks. The convolutional architecture
is particularly well-suited for image data, representing a key machine learning
approach.

Paper [3] discusses transfer learning for medical image classification, showing
how pre-trained models can be adapted for specific classification problems. This
is an important practical technique in machine learning.

Paper [4] explores feature selection methods, which are crucial preprocessing steps
in classification pipelines. Techniques like PCA and LDA help improve classification
performance by reducing dimensionality.

All papers demonstrate different aspects of machine learning for classification,
from algorithm selection to feature engineering to domain-specific applications.

--------------------------------------------------------------------------------
END OF RESULTS
--------------------------------------------------------------------------------

❯
```

---

## Example 2: Changing Settings

**User Input:**
```
❯ mode simple
```

**System Response:**
```
✓ Generation mode set to: simple

❯
```

**User Input:**
```
❯ results 3
```

**System Response:**
```
✓ Number of results set to: 3

❯
```

**User Input:**
```
❯ deep learning architectures
```

**System Response:**
```
================================================================================
SEARCH QUERY
================================================================================
Query: deep learning architectures
Time: 2025-12-09 15:32:10

Retrieving documents: [████████████████████████████████████████] 100/100 (100.0%)

RETRIEVAL STATISTICS
--------------------------------------------------------------------------------
✓ Retrieved: 3 chunks from 3 unique papers
✓ Average Similarity: 0.445
✓ Retrieval Time: 178.22ms

Generating explanation: [████████████████████████████████████████] 100/100 (100.0%)


[... retrieval results ...]

RELEVANCE ANALYSIS
--------------------------------------------------------------------------------
1. This paper proposes a novel deep learning architecture for image recognition with improved accuracy.
2. This paper discusses optimization techniques for training deep neural networks efficiently.
3. This paper presents a transformer-based architecture for natural language processing tasks.

--------------------------------------------------------------------------------
END OF RESULTS
--------------------------------------------------------------------------------

❯
```

---

## Example 3: Saving Results

**User Input:**
```
❯ format markdown
```

**System Response:**
```
✓ Output format set to: markdown

❯
```

**User Input:**
```
❯ neural networks
```

**System Response:**
```
[... query results in markdown format ...]

❯
```

**User Input:**
```
❯ save neural_networks_analysis.md
```

**System Response:**
```
✓ Results saved to neural_networks_analysis.md

❯
```

---

## Example 4: Viewing History

**User Input:**
```
❯ history
```

**System Response:**
```

======================================================================
QUERY HISTORY
======================================================================

1. Query: machine learning for classification
   Results: 5 | Mode: detailed

2. Query: deep learning architectures
   Results: 3 | Mode: simple

3. Query: neural networks
   Results: 3 | Mode: simple

❯
```

---

## Example 5: Getting Help

**User Input:**
```
❯ help
```

**System Response:**
```

Command Reference:

QUERYING:
  query <text>           Search for papers matching your query
  <text>                 You can also just type your query directly

CONFIGURATION:
  mode detailed          Use detailed explanation mode (default)
  mode simple            Use simple one-sentence summary mode
  format text            Plain text output with colors (default)
  format json            Structured JSON output
  format markdown        Markdown formatted output
  format summary         Brief summary view
  results <n>            Set number of results (1-20)

UTILITIES:
  history                Show all queries from this session
  save <filename>        Save last result to file
  clear                  Clear the terminal screen
  help                   Show this help message
  exit                   Exit the program

EXAMPLES:
  > machine learning for text classification
  > mode simple
  > What are recent advances in computer vision?
  > format json
  > results 10
  > save my_results.txt

❯
```

---

## Example 6: Exiting

**User Input:**
```
❯ exit
```

**System Response:**
```

Thank you for using Academic RAG System!
```

---

## Single Query Mode Examples

Instead of interactive mode, you can run single queries:

### Example 1: Basic Single Query

```bash
python rag_cli.py --query "machine learning"
```

### Example 2: With Options

```bash
python rag_cli.py \
    --query "neural networks" \
    --mode simple \
    --num-results 10 \
    --format json
```

### Example 3: Save to File

```bash
python rag_cli.py \
    --query "deep learning for computer vision" \
    --save cv_papers.md
```

### Example 4: No Colors (for Logging)

```bash
python rag_cli.py \
    --query "optimization algorithms" \
    --no-color \
    > logfile.txt
```

### Example 5: Batch Processing

```bash
#!/bin/bash
# batch_queries.sh

topics=("machine learning" "deep learning" "computer vision" "natural language processing")

for topic in "${topics[@]}"; do
    echo "Querying: $topic"
    python rag_cli.py \
        -q "$topic" \
        -m simple \
        -n 10 \
        -f json \
        -s "results/${topic// /_}.json"
done
```

---

## Tips for Best Experience

### Query Formulation

**Good Queries:**
```
❯ neural networks for image classification
❯ optimization algorithms for deep learning
❯ transfer learning in computer vision
❯ attention mechanisms in transformers
```

**Less Effective Queries:**
```
❯ AI                    # Too broad
❯ papers                # Not topic-specific
❯ good machine learning # Vague
```

### Workflow Suggestions

**Literature Review:**
```
❯ mode detailed
❯ results 10
❯ format markdown
❯ [your topic query]
❯ save topic_literature_review.md
```

**Quick Scanning:**
```
❯ mode simple
❯ results 15
❯ format summary
❯ [broad topic query]
```

**Data Collection:**
```
❯ format json
❯ [query 1]
❯ save query1.json
❯ [query 2]
❯ save query2.json
```

---

## Common Workflows

### Workflow 1: Exploratory Research

```
1. Start with broad query in detailed mode
2. Review results
3. Switch to simple mode for faster scanning
4. Try related queries
5. Save interesting results
6. Check history to see what you've covered
```

### Workflow 2: Targeted Search

```
1. Start with specific query
2. Increase results if needed (results 15)
3. Switch to markdown format
4. Save to file for documentation
```

### Workflow 3: Batch Analysis

```
1. Use single-query mode with JSON output
2. Process multiple queries via script
3. Analyze JSON data with tools (jq, pandas)
```

---

This example session demonstrates the flexibility and power of the RAG CLI.
Whether you're doing exploratory research, conducting literature reviews, or
collecting data, the CLI provides a natural and efficient interface to your
academic paper corpus.

For more information, see:
- **CLI_GUIDE.md** - Comprehensive documentation
- **CLI_QUICK_REFERENCE.md** - Quick command reference
- **README.md** - Project overview and setup
