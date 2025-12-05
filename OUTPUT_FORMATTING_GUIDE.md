# Output Formatting Guide

This guide explains the output formatting capabilities of the Academic RAG System.

## Overview

The output formatting system provides multiple ways to display and save RAG system results:

- **Colored Terminal Output** - Beautiful, readable output with color-coded elements
- **JSON Format** - Structured data for programmatic access
- **Markdown Format** - Clean format for documentation and reports
- **Summary Format** - Quick overview of results

## Features

### 1. Colored Terminal Output

The default output format uses ANSI color codes for improved readability:

- **Blue headers** for major sections
- **Cyan subheaders** for subsections
- **Green checkmarks** for success messages and statistics
- **Color-coded similarity scores**:
  - Green (≥0.8) - Highly similar
  - Yellow (0.6-0.8) - Moderately similar
  - Red (<0.6) - Less similar

Example:
```bash
python demo_formatting.py --query "machine learning"
```

### 2. JSON Format

Structured output suitable for APIs, data processing, or integration with other tools:

```bash
python demo_formatting.py --query "neural networks" --format json
```

JSON structure:
```json
{
  "timestamp": "2025-12-05T16:46:06.975689",
  "query": "machine learning for document classification",
  "retrieval": {
    "num_documents": 3,
    "documents": [...],
    "statistics": {
      "num_retrieved": 3,
      "num_unique_sources": 3,
      "avg_similarity_score": 0.747,
      "retrieval_time_ms": 42.5
    }
  },
  "explanation": "..."
}
```

### 3. Markdown Format

Clean format for documentation, reports, and sharing results:

```bash
python demo_formatting.py --query "AI ethics" --format markdown
```

Perfect for:
- Research notes
- Project documentation
- Sharing with colleagues
- Including in reports

### 4. Summary Format

Condensed view showing key information:

```bash
python demo_formatting.py --query "deep learning" --format summary
```

Displays:
- Query information
- Number of documents found
- Top 5 source papers
- Brief key findings

## Usage Examples

### Basic Query
```bash
python demo_formatting.py --query "information retrieval systems"
```

### Save Results to File
```bash
python demo_formatting.py --query "NLP techniques" --save outputs/nlp_results.txt
```

### Get More Results
```bash
python demo_formatting.py --query "deep learning" --num-results 10
```

### Disable Colors (for piping to files)
```bash
python demo_formatting.py --query "AI" --no-color > results.txt
```

### Hide Document Excerpts
```bash
python demo_formatting.py --query "ML models" --no-excerpts
```

### Combine Options
```bash
python demo_formatting.py \
  --query "transformer models" \
  --format markdown \
  --num-results 5 \
  --save outputs/transformers.md
```

## Output Components

### Query Information
- Search query
- Timestamp
- Number of results

### Retrieval Statistics
- Number of chunks retrieved
- Number of unique source papers
- Average similarity score
- Retrieval time (milliseconds)

### Retrieved Documents
For each document:
- Source filename
- Similarity score (color-coded)
- Text excerpt (optional)
- Chunk index

### Relevance Analysis
LLM-generated analysis including:
- Relevance level (Highly/Moderately/Not Relevant)
- Detailed explanation
- Key concepts from each paper

## Programmatic Usage

You can also use the formatting classes in your own code:

### Basic Example
```python
from src.output_formatter import OutputFormatter

formatter = OutputFormatter(use_colors=True)

# Format query information
print(formatter.format_query_info("my query"))

# Format retrieval statistics
stats = {
    "num_retrieved": 5,
    "num_unique_sources": 4,
    "avg_similarity_score": 0.75,
    "retrieval_time_ms": 120.5
}
print(formatter.format_retrieval_stats(stats))

# Format complete results
output = formatter.format_complete_result(
    query="my query",
    documents=documents,
    explanation=explanation,
    stats=stats,
    show_document_text=True
)
print(output)
```

### Using MarkdownFormatter
```python
from src.output_formatter import MarkdownFormatter

md_formatter = MarkdownFormatter()
output = md_formatter.format_complete_result(
    query="my query",
    documents=documents,
    explanation=explanation,
    stats=stats
)

# Save to file
from pathlib import Path
md_formatter.save_to_file(output, Path("output.md"), "md")
```

### Progress Indicators
```python
formatter = OutputFormatter()

for i in range(0, 101, 10):
    print(f"\r{formatter.format_progress(i, 100, 'Processing')}",
          end='', flush=True)
```

### Success and Error Messages
```python
formatter = OutputFormatter()

# Success message
print(formatter.format_success("Task completed successfully"))

# Error message
print(formatter.format_error("Something went wrong", "ERROR"))

# Warning message
print(formatter.format_error("Low similarity scores", "WARNING"))
```

## Customization

### Disable Colors
For environments that don't support ANSI colors:
```python
formatter = OutputFormatter(use_colors=False)
```

### Custom Headers
```python
# Default equals sign border
print(formatter.format_header("My Header"))

# Custom border character
print(formatter.format_header("My Header", char="-"))
```

### Custom Excerpts
Control excerpt length when displaying documents:
```python
# In output_formatter.py, modify this line:
excerpt = text[:200]  # Change 200 to your preferred length
```

## Output File Formats

### Text Files (.txt)
Plain text with ANSI codes removed (if colors disabled)
- Good for: Basic documentation, logs

### JSON Files (.json)
Structured data with proper indentation
- Good for: APIs, data processing, archiving

### Markdown Files (.md)
Clean markdown formatting
- Good for: Documentation, reports, GitHub

## Best Practices

1. **Use colored output for terminal viewing** - Makes results easier to scan
2. **Use JSON for programmatic access** - Parse and process results in code
3. **Use Markdown for documentation** - Share results in readable format
4. **Use summary format for quick checks** - Fast overview of results
5. **Save important results** - Keep records of successful queries
6. **Disable colors when piping** - Prevents ANSI codes in text files

## Statistics Explained

### Number Retrieved
Total number of text chunks retrieved from the vector database

### Unique Sources
Number of distinct source papers (multiple chunks may come from same paper)

### Average Similarity Score
Mean similarity score across all retrieved chunks (0.0 to 1.0)
- 0.8-1.0: Highly relevant
- 0.6-0.8: Moderately relevant
- 0.0-0.6: Less relevant

### Retrieval Time
Time taken to query the vector database (in milliseconds)

## Troubleshooting

### Colors Not Showing
- Check that your terminal supports ANSI colors
- Try using a different terminal emulator
- Use `--no-color` flag if needed

### Output Too Long
- Use `--no-excerpts` to hide document text
- Use `--format summary` for condensed view
- Reduce `--num-results` value

### File Not Saving
- Check that the output directory exists
- Verify write permissions
- Check disk space

### Encoding Issues
- All files are saved with UTF-8 encoding
- Ensure your terminal supports UTF-8
- Check locale settings: `echo $LANG`

## Future Enhancements

Potential improvements for output formatting:

- [ ] HTML output format with CSS styling
- [ ] PDF export capability
- [ ] Custom color schemes
- [ ] Configurable output templates
- [ ] Chart/graph visualizations of similarity scores
- [ ] Side-by-side comparison format
- [ ] Export to CSV for spreadsheet analysis

## Related Documentation

- See `demo_formatting.py` for usage examples
- See `src/output_formatter.py` for implementation details
- See `PROGRESS.md` for project status
