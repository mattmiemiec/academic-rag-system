# Academic RAG System
## By Matthew Miemiec
<b>Yonsei University</b>
<i>2025-2 LIS8040: Text Understanding and Artificial Intelligence</i>

This repo contains the completed independent project that I developed while attending LIS8040 at Yonsei University. 

The result is a fully functional local RAG (Retrieval Augmented Generation) that, instead of relying solely on data or fine-tuning an LLM, queries external sources for more current results. This RAG leverages the power of Ollama and Mixtral 8x7b to run an entirely local, private RAG prototype.

The star of the show is **rag_cli.py**, which can be used to initiate the RAG and retrieve results for queries based on the 75 articles in its chroma vector database. 

**Key Features:**
- 🔍 **Semantic Search**: Find papers by meaning, not just keywords
- 🤖 **AI Explanations**: Get relevance explanations powered by Mixtral 8x7b
- 💬 **Interactive Mode**: Natural conversation-style querying
- 📊 **Multiple Formats**: Output as text, JSON, markdown, or summary
- 📝 **Query History**: Track all queries in your session
- 💾 **Export Results**: Save outputs to files

#### Note:
This was tested on a MacBook Pro M4 Max with 48 GB of RAM. Your results may vary depending on your machine.

### Quick Start
1. Pull the GitHub and set up a Python virtual environment.
`cd ~/Local/academic_rag_system`
`source venv/bin/activate`

2. Install Ollama if needed, and download the mixtral:8x7b model.
-> Install Ollama from https://ollama.ai
`ollama pull mixtral:8x7b`

3. Make sure the chroma_db/ file exists and has embeddings.

4. Install requirements
`pip install -r requirements.txt`

#### Launch Interactive Mode
`python rag_cli.py`

#### Single Query Mode
`python rag_cli.py --query "machine learning for classification"`

**Basic query**
`python rag_cli.py --query "machine learning"`

**With options**
`python rag_cli.py -q "neural networks" -m simple -n 10 -f json`

**Save results**
`python rag_cli.py -q "deep learning" -s results.txt`


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

## Troubleshooting

### Common Issues

#### "Chroma database not found"
**Problem**: Database doesn't exist at specified path

**Solution**:
Check to see if chroma_db exits:
`ls -la chroma_db/`

If missing, regenerate embeddings
`python -m src.embeddings`


#### "Connection refused" from Ollama
**Problem**: Ollama is not running

**Solution**:
Start Ollama in another terminal
`ollama serve`

Or check if it's running
`ps aux | grep ollama`


#### "ModuleNotFoundError"
**Problem**: Virtual environment not activated

**Solution**:
`source venv/bin/activate`
`python rag_cli.py`


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
** Might be due to the limited scope of the source material: only 75 papers from arXiv 2509

** Credit must be given where credit is due: I am still a novice at programming and especially RAG development. Therefore, I relied heavily on Claude Code to guide me through this project. However, the ideas are my own, and I actively participated in the project, making decisions and learning how each component functions and fits together. 
