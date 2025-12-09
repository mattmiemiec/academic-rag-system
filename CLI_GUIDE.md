# Academic RAG System - CLI Guide

**Interactive Command-Line Interface for Querying Academic Papers**

Version: 1.0
Last Updated: December 9, 2025

---

## Overview

The Academic RAG System CLI (`rag_cli.py`) provides an interactive interface for querying 75 academic papers using semantic search and LLM-based explanations. It combines vector search (embeddings) with natural language generation (Mixtral 8x7b) to help you discover relevant research.

**Key Features:**
- 🔍 **Semantic Search**: Find papers by meaning, not just keywords
- 🤖 **AI Explanations**: Get relevance explanations powered by Mixtral 8x7b
- 💬 **Interactive Mode**: Natural conversation-style querying
- 📊 **Multiple Formats**: Output as text, JSON, markdown, or summary
- 📝 **Query History**: Track all queries in your session
- 💾 **Export Results**: Save outputs to files

---

## Quick Start

### Prerequisites

1. **Virtual Environment**: Activate the virtual environment
   ```bash
   cd ~/Local/academic_rag_system
   source venv/bin/activate
   ```

2. **Ollama Running**: Make sure Ollama is running with Mixtral
   ```bash
   # In another terminal
   ollama serve

   # Verify Mixtral is available
   ollama list | grep mixtral
   ```

3. **Database Ready**: Ensure `chroma_db/` exists with embeddings

### Launch Interactive Mode

```bash
python rag_cli.py
```

You'll see a welcome screen with available commands. Just type your query!

### Single Query Mode

```bash
python rag_cli.py --query "machine learning for classification"
```

---

## Usage Modes

### 1. Interactive Mode (Recommended)

Launch with no arguments for the full interactive experience:

```bash
python rag_cli.py
```

**Example Session:**
```
❯ neural networks for image classification
[System retrieves documents and generates explanation]

❯ mode simple
✓ Generation mode set to: simple

❯ deep learning architectures
[System retrieves documents with simple explanations]

❯ format json
✓ Output format set to: json

❯ computer vision techniques
[System outputs JSON-formatted results]

❯ save my_results.json
✓ Results saved to my_results.json

❯ history
QUERY HISTORY
1. Query: neural networks for image classification
   Results: 5 | Mode: detailed

2. Query: deep learning architectures
   Results: 5 | Mode: simple

3. Query: computer vision techniques
   Results: 5 | Mode: simple

❯ exit
Thank you for using Academic RAG System!
```

### 2. Single Query Mode

Run one query and exit:

```bash
# Basic query
python rag_cli.py --query "machine learning"

# With options
python rag_cli.py -q "neural networks" -m simple -n 10 -f json

# Save results
python rag_cli.py -q "deep learning" -s results.txt
```

---

## Commands Reference

### Interactive Mode Commands

| Command | Arguments | Description | Example |
|---------|-----------|-------------|---------|
| `<query>` | text | Search for papers (direct query) | `machine learning` |
| `query` | text | Search for papers (explicit) | `query neural networks` |
| `mode` | detailed\|simple | Set generation mode | `mode simple` |
| `format` | text\|json\|markdown\|summary | Set output format | `format json` |
| `results` | number (1-20) | Set number of results | `results 10` |
| `history` | - | Show query history | `history` |
| `save` | filename | Save last result to file | `save output.txt` |
| `help` | - | Show help message | `help` |
| `clear` | - | Clear terminal screen | `clear` |
| `exit` | - | Exit the program | `exit` or `quit` |

### Command-Line Options

| Option | Short | Values | Default | Description |
|--------|-------|--------|---------|-------------|
| `--query` | `-q` | text | - | Single query (non-interactive) |
| `--mode` | `-m` | detailed\|simple | detailed | Generation mode |
| `--num-results` | `-n` | 1-20 | 5 | Number of results |
| `--format` | `-f` | text\|json\|markdown\|summary | text | Output format |
| `--save` | `-s` | filepath | - | Save output to file |
| `--no-color` | - | flag | false | Disable colored output |
| `--chroma-path` | - | path | ./chroma_db | Path to database |
| `--help` | `-h` | - | - | Show help message |

---

## Output Formats

### 1. Text (Default)

Colored, formatted output for terminal viewing.

**Features:**
- Color-coded similarity scores (green/yellow/red)
- Progress indicators
- Retrieval statistics
- Full explanations with document excerpts

**Example:**
```
================================================================================
SEARCH QUERY
================================================================================
Query: machine learning for classification
Time: 2025-12-09 15:30:45

RETRIEVAL STATISTICS
--------------------------------------------------------------------------------
✓ Retrieved: 5 chunks from 4 unique papers
✓ Average Similarity: 0.421
✓ Retrieval Time: 189.34ms

RETRIEVED DOCUMENTS (5)
--------------------------------------------------------------------------------

[1] 2509.12345v1.pdf
    Similarity: 0.512 ✓
    Excerpt: This paper presents a novel approach to classification...

RELEVANCE ANALYSIS
--------------------------------------------------------------------------------
The retrieved papers discuss various machine learning techniques for classification...
```

### 2. JSON

Structured data format for programmatic processing.

**Usage:**
```bash
python rag_cli.py -q "neural networks" -f json > output.json
```

**Structure:**
```json
{
  "query": "neural networks",
  "timestamp": "2025-12-09T15:30:45",
  "retrieval_stats": {
    "num_documents": 5,
    "unique_sources": 4,
    "avg_similarity": 0.421,
    "retrieval_time_ms": 189.34
  },
  "documents": [
    {
      "rank": 1,
      "source": "2509.12345v1.pdf",
      "similarity": 0.512,
      "text": "..."
    }
  ],
  "explanation": "..."
}
```

### 3. Markdown

Clean markdown formatting for documentation.

**Usage:**
```bash
python rag_cli.py -q "deep learning" -f markdown -s report.md
```

**Features:**
- Standard markdown headers
- Numbered lists
- Code blocks
- Easy to integrate into documentation

### 4. Summary

Brief overview of results.

**Usage:**
```bash
python rag_cli.py -q "computer vision" -f summary
```

**Example:**
```
QUERY SUMMARY
Query: computer vision
Documents Found: 5 unique papers
Key Finding: The papers focus on computer vision applications...

Top Sources:
1. 2509.12345v1.pdf
2. 2509.23456v1.pdf
3. 2509.34567v1.pdf
```

---

## Generation Modes

### Detailed Mode (Default)

Provides comprehensive analysis with:
- Relevance explanation for each paper
- Key concepts and methodologies
- How papers relate to the query
- 3-5 paragraphs of analysis

**Best For:**
- Research literature reviews
- Understanding paper relevance
- Detailed exploration

**Example:**
```
❯ mode detailed
❯ machine learning for healthcare
```

### Simple Mode

Provides concise one-sentence summaries:
- Quick relevance assessment per paper
- Numbered list format
- Fast generation (~5-10 seconds)

**Best For:**
- Quick scanning of results
- Batch querying
- Getting overview before detailed analysis

**Example:**
```
❯ mode simple
❯ machine learning for healthcare

RELEVANCE ANALYSIS
1. This paper proposes ML techniques for disease prediction in healthcare.
2. This paper discusses data privacy but does not focus on ML.
3. This paper presents a comprehensive ML framework for patient diagnosis.
```

---

## Examples

### Example 1: Research Literature Review

**Goal**: Find papers about neural networks for image classification

```bash
❯ neural networks for image classification
❯ results 10
❯ mode detailed
❯ save neural_networks_review.md
```

### Example 2: Quick Topic Scan

**Goal**: Get a quick overview of papers mentioning "optimization"

```bash
python rag_cli.py -q "optimization algorithms" -m simple -n 15 -f summary
```

### Example 3: Batch Processing

**Goal**: Query multiple topics and save as JSON for analysis

```bash
# Create a script
for topic in "machine learning" "deep learning" "computer vision"; do
    python rag_cli.py -q "$topic" -f json -s "results_${topic// /_}.json"
done
```

### Example 4: Finding Specific Methods

**Goal**: Find papers using specific techniques

```bash
❯ transformer models for natural language processing
❯ results 10
❯ format markdown
❯ save transformer_papers.md
```

### Example 5: Exploratory Session

**Goal**: Interactive exploration with settings changes

```bash
❯ machine learning

[Review results]

❯ mode simple
❯ results 10
❯ deep learning architectures

[Quick scan]

❯ mode detailed
❯ results 5
❯ convolutional neural networks
❯ format markdown
❯ save cnn_analysis.md

❯ history
```

---

## Tips and Best Practices

### Query Formulation

**Good Queries:**
- `"neural networks for image classification"` - Specific with context
- `"deep learning architectures"` - Clear topic
- `"optimization algorithms for machine learning"` - Detailed intent

**Less Effective Queries:**
- `"AI"` - Too broad
- `"paper about stuff"` - Vague
- `"good research"` - Not topic-focused

**Pro Tips:**
1. **Use phrases**: Multi-word queries work better than single words
2. **Add context**: "X for Y" queries are very effective
3. **Be specific**: "convolutional neural networks" > "networks"
4. **Try variations**: If results aren't good, rephrase your query

### Performance Optimization

1. **Start with fewer results**: Use `results 5` initially, increase if needed
2. **Use simple mode for scanning**: Switch to `mode simple` for quick exploration
3. **Save frequently**: Use `save` to preserve good results
4. **Check history**: Use `history` to track what you've searched

### Output Format Selection

| Use Case | Recommended Format |
|----------|-------------------|
| Terminal viewing | text (default) |
| Programming/analysis | json |
| Documentation | markdown |
| Quick overview | summary |
| Sharing with others | markdown or text |

### Session Management

```bash
# Start a research session
python rag_cli.py

# Set your preferences
❯ mode detailed
❯ results 10
❯ format markdown

# Query and save incrementally
❯ topic 1 query
❯ save topic1.md

❯ topic 2 query
❯ save topic2.md

# Review your work
❯ history

# Exit
❯ exit
```

---

## Troubleshooting

### Common Issues

#### "Chroma database not found"

**Problem**: Database doesn't exist at specified path

**Solution**:
```bash
# Check if database exists
ls -la chroma_db/

# If missing, regenerate embeddings
python -m src.embeddings
```

#### "Connection refused" from Ollama

**Problem**: Ollama is not running

**Solution**:
```bash
# Start Ollama in another terminal
ollama serve

# Or check if it's running
ps aux | grep ollama
```

#### "ModuleNotFoundError"

**Problem**: Virtual environment not activated

**Solution**:
```bash
source venv/bin/activate
python rag_cli.py
```

#### Slow responses

**Problem**: First query is slow due to model loading

**Solution**:
- First query loads models (~5-10 seconds)
- Subsequent queries are much faster
- Use `mode simple` for faster generation

#### No relevant results

**Problem**: Query too specific or documents don't match

**Solution**:
- Try broader queries
- Use different phrasing
- Increase number of results: `results 15`
- Check what's in the corpus: only 75 papers from arXiv 2509

---

## Advanced Usage

### Custom Database Path

```bash
python rag_cli.py --chroma-path /path/to/custom/chroma_db
```

### Disable Colors for Logging

```bash
python rag_cli.py --no-color > logfile.txt
```

### Piping and Redirection

```bash
# Save full output
python rag_cli.py -q "machine learning" > full_output.txt

# JSON for processing
python rag_cli.py -q "deep learning" -f json | jq '.documents[].source'

# Multiple queries
cat queries.txt | while read query; do
    python rag_cli.py -q "$query" -f summary
done
```

### Integration with Other Tools

**Example: Extract just paper titles**
```bash
python rag_cli.py -q "neural networks" -f json | \
    jq -r '.documents[].source' | \
    sort | uniq
```

**Example: Count unique papers per query**
```bash
for query in "ML" "DL" "CV"; do
    count=$(python rag_cli.py -q "$query" -f json | \
            jq '.retrieval_stats.unique_sources')
    echo "$query: $count papers"
done
```

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Cancel current operation (returns to prompt) |
| `Ctrl+D` | Exit program (same as `exit`) |
| `↑` / `↓` | Navigate command history (terminal feature) |

---

## Output Files

### File Naming Recommendations

```bash
# Descriptive names
❯ save ml_classification_papers.md

# Timestamped
❯ save results_2025-12-09.txt

# Topic-based organization
❯ save computer_vision/cnn_analysis.md
❯ save nlp/transformer_papers.json
```

### File Formats by Extension

The system auto-detects format from extension:
- `.txt` → Text format
- `.json` → JSON format
- `.md` → Markdown format

Or specify explicitly:
```bash
python rag_cli.py -q "..." -f json -s output.txt  # Force JSON in .txt file
```

---

## Performance Metrics

Typical performance on M1 Mac:

| Operation | Time |
|-----------|------|
| Initial load | 5-10 seconds |
| Vector search | 150-250ms |
| Detailed generation | 15-30 seconds |
| Simple generation | 5-10 seconds |
| JSON export | <100ms |

**Optimization Tips:**
- First query is slowest (model loading)
- Use `mode simple` for 2-3x faster generation
- Smaller `num_results` = faster retrieval
- JSON/summary formats = no generation overhead

---

## Comparison with Other Tools

### `rag_cli.py` vs `demo_formatting.py`

| Feature | rag_cli.py | demo_formatting.py |
|---------|------------|-------------------|
| Interactive mode | ✅ Yes | ❌ No |
| Settings changes | ✅ On-the-fly | ❌ Command-line only |
| Query history | ✅ Yes | ❌ No |
| Generation modes | ✅ Both | ✅ Both |
| Best for | Exploration | Single queries |

**When to use `rag_cli.py`**:
- Interactive research sessions
- Multiple related queries
- Experimenting with settings

**When to use `demo_formatting.py`**:
- Scripting and automation
- Single specific query
- Simpler interface

---

## Future Enhancements

Potential features for future versions:

- [ ] Query suggestions based on corpus
- [ ] Bookmark/favorite papers
- [ ] Export query history to file
- [ ] Filter by date/topic
- [ ] Similarity threshold configuration
- [ ] Multi-query batch mode
- [ ] Source deduplication toggle
- [ ] Relevance feedback (mark papers as relevant/not)
- [ ] Paper metadata display (authors, dates)
- [ ] Citation export (BibTeX format)

---

## Support and Contributing

### Getting Help

1. **Help command**: Type `help` in interactive mode
2. **Documentation**: See `README.md` for system overview
3. **Evaluation**: See `EVALUATION_SUMMARY.md` for performance metrics
4. **Issues**: Check GitHub issues (when published)

### Feedback

Found a bug or have a suggestion? Please create an issue with:
- What you were trying to do
- What happened vs. what you expected
- System info (OS, Python version)
- Steps to reproduce

---

## Summary

The Academic RAG System CLI provides a powerful, flexible interface for semantic search over academic papers. Whether you're doing exploratory research, conducting literature reviews, or looking for specific methodologies, the CLI offers:

✅ **Natural querying** - Just type what you're looking for
✅ **Flexible output** - Multiple formats for different needs
✅ **AI-powered explanations** - Understand paper relevance
✅ **Interactive exploration** - Change settings on the fly
✅ **Export capabilities** - Save and share results

**Start exploring your academic corpus today!**

```bash
cd ~/Local/academic_rag_system
source venv/bin/activate
python rag_cli.py
```

---

**Version**: 1.0
**Last Updated**: December 9, 2025
**Author**: Matt (LIS8040 Independent Project)
