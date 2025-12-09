# RAG CLI Quick Reference

## Launch

```bash
cd ~/Local/academic_rag_system
source venv/bin/activate
python rag_cli.py
```

## Common Commands

| Command | What it Does |
|---------|-------------|
| `<your query>` | Just type your search query |
| `mode simple` | Quick one-sentence summaries |
| `mode detailed` | Full explanations (default) |
| `format json` | JSON output |
| `format markdown` | Markdown output |
| `results 10` | Get 10 results instead of 5 |
| `save file.txt` | Save last result to file |
| `history` | Show all queries this session |
| `help` | Show help |
| `exit` | Quit |

## Single Query (No Interactive)

```bash
# Basic
python rag_cli.py -q "your query here"

# With options
python rag_cli.py -q "neural networks" -m simple -n 10 -f json

# Save to file
python rag_cli.py -q "machine learning" -s results.txt
```

## Example Session

```
❯ machine learning for classification
  [Shows 5 results with detailed explanation]

❯ mode simple
  ✓ Generation mode set to: simple

❯ results 10
  ✓ Number of results set to: 10

❯ deep learning architectures
  [Shows 10 results with simple summaries]

❯ save dl_papers.txt
  ✓ Results saved to dl_papers.txt

❯ exit
```

## Tips

- **First query is slow** (loading models) - be patient!
- **Use phrases** not single words: "neural networks for NLP" > "networks"
- **Try simple mode** first to scan, then detailed for depth
- **Increase results** if not finding what you need: `results 15`
- **Save good results** as you go: `save topic_name.md`

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Database not found" | Check `chroma_db/` exists |
| "Connection refused" | Start Ollama: `ollama serve` |
| "Module not found" | Activate venv: `source venv/bin/activate` |
| Slow response | First query loads models (~10 sec) |

## Output Formats

- **text** - Colored terminal output (default, best for viewing)
- **json** - Structured data (best for processing)
- **markdown** - Documentation format (best for sharing)
- **summary** - Brief overview (best for quick scan)

---

**More Details**: See `CLI_GUIDE.md` for complete documentation
