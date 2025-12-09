#!/usr/bin/env python3
"""
Academic RAG System - Interactive Command-Line Interface

A comprehensive CLI for querying academic papers using semantic search and LLM-based explanations.

Usage:
    # Interactive mode
    python rag_cli.py

    # Single query mode
    python rag_cli.py --query "machine learning for classification"

    # Advanced options
    python rag_cli.py --query "neural networks" --mode detailed --num-results 10 --format json
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, List, Dict

from src.retrieval import get_retriever
from src.generation import ExplanationGenerator
from src.output_formatter import OutputFormatter, MarkdownFormatter


class RAGCli:
    """Interactive CLI for the Academic RAG System."""

    def __init__(self, chroma_path: str, use_colors: bool = True):
        """
        Initialize the CLI application.

        Args:
            chroma_path: Path to Chroma vector database
            use_colors: Whether to use colored terminal output
        """
        self.chroma_path = chroma_path
        self.use_colors = use_colors
        self.formatter = OutputFormatter(use_colors=use_colors)
        self.markdown_formatter = MarkdownFormatter()

        # Initialize components (lazy loading for faster startup)
        self.retriever = None
        self.generator = None

        # Session state
        self.query_history = []

    def initialize_components(self):
        """Initialize retriever and generator (lazy loading)."""
        if self.retriever is None:
            print(self.formatter.format_progress(0, 100, "Loading RAG system"))
            self.retriever = get_retriever("semantic", self.chroma_path)
            print(f"\r{self.formatter.format_progress(50, 100, 'Loading RAG system')}", end="")
            self.generator = ExplanationGenerator()
            print(f"\r{self.formatter.format_progress(100, 100, 'Loading RAG system')}")
            print(self.formatter.format_success("✓ RAG system initialized\n"))

    def display_welcome(self):
        """Display welcome message."""
        welcome = """
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
"""
        print(welcome)

    def display_help(self):
        """Display help information."""
        help_text = """
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
"""
        print(help_text)

    def run_query(
        self,
        query: str,
        num_results: int = 5,
        generation_mode: str = "detailed",
        output_format: str = "text"
    ) -> Optional[Dict]:
        """
        Execute a search query and generate explanations.

        Args:
            query: Search query
            num_results: Number of results to retrieve
            generation_mode: 'detailed' or 'simple'
            output_format: Output format type

        Returns:
            Dictionary with query results or None on error
        """
        # Initialize if needed
        self.initialize_components()

        # Record query
        self.query_history.append({
            'query': query,
            'num_results': num_results,
            'mode': generation_mode
        })

        # Display query info
        print(self.formatter.format_query_info(query))

        # Retrieve documents
        print(self.formatter.format_progress(0, 100, "Retrieving documents"), end="", flush=True)
        documents, stats = self.retriever.retrieve_with_stats(query, k=num_results)
        print(f"\r{self.formatter.format_progress(100, 100, 'Retrieving documents')}")

        if not documents:
            print(self.formatter.format_error("No documents found for query", "WARNING"))
            return None

        print(self.formatter.format_retrieval_stats(stats))

        # Generate explanation
        print(self.formatter.format_progress(0, 100, "Generating explanation"), end="", flush=True)

        if generation_mode == "simple":
            explanation = self.generator.generate_simple(query, documents)
        else:
            explanation = self.generator.generate(query, documents)

        print(f"\r{self.formatter.format_progress(100, 100, 'Generating explanation')}\n")

        # Prepare result
        result = {
            'query': query,
            'documents': documents,
            'explanation': explanation,
            'stats': stats
        }

        # Format and display output
        self.display_result(result, output_format)

        return result

    def display_result(self, result: Dict, output_format: str = "text"):
        """
        Display query results in specified format.

        Args:
            result: Query result dictionary
            output_format: Format type (text, json, markdown, summary)
        """
        formatter = self.markdown_formatter if output_format == "markdown" else self.formatter

        if output_format == "json":
            output = formatter.to_json(
                result['query'],
                result['documents'],
                result['explanation'],
                result['stats']
            )
        elif output_format == "summary":
            top_sources = [doc['source'] for doc in result['documents'][:5]]
            key_finding = result['explanation'].split('\n')[0] if result['explanation'] else "See analysis"
            output = formatter.format_summary(
                query=result['query'],
                num_documents=len(result['documents']),
                top_sources=top_sources,
                key_findings=key_finding
            )
        else:  # text or markdown
            output = formatter.format_complete_result(
                query=result['query'],
                documents=result['documents'],
                explanation=result['explanation'],
                stats=result['stats'],
                show_document_text=True
            )

        print(output)

        # Store for potential saving
        self.last_output = output
        self.last_format = output_format

    def save_last_result(self, filepath: str) -> bool:
        """
        Save the last query result to a file.

        Args:
            filepath: Path to save file

        Returns:
            True if successful, False otherwise
        """
        if not hasattr(self, 'last_output'):
            print(self.formatter.format_error("No results to save. Run a query first.", "WARNING"))
            return False

        try:
            save_path = Path(filepath)
            save_path.parent.mkdir(parents=True, exist_ok=True)

            if self.formatter.save_to_file(self.last_output, save_path, self.last_format):
                print(self.formatter.format_success(f"✓ Results saved to {filepath}"))
                return True
            else:
                print(self.formatter.format_error(f"Failed to save to {filepath}"))
                return False
        except Exception as e:
            print(self.formatter.format_error(f"Error saving file: {str(e)}"))
            return False

    def show_history(self):
        """Display query history for this session."""
        if not self.query_history:
            print(self.formatter.format_error("No queries in history yet", "INFO"))
            return

        print("\n" + "="*70)
        print("QUERY HISTORY")
        print("="*70 + "\n")

        for i, item in enumerate(self.query_history, 1):
            print(f"{i}. Query: {item['query']}")
            print(f"   Results: {item['num_results']} | Mode: {item['mode']}")
            print()

    def clear_screen(self):
        """Clear the terminal screen."""
        import os
        os.system('clear' if os.name != 'nt' else 'cls')

    def interactive_mode(self):
        """Run the CLI in interactive mode."""
        self.display_welcome()

        # Settings
        num_results = 5
        generation_mode = "detailed"
        output_format = "text"

        while True:
            try:
                # Get user input
                user_input = input(self.formatter.format_query_prompt("❯ ")).strip()

                if not user_input:
                    continue

                # Parse command
                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""

                # Handle commands
                if command in ["exit", "quit", "q"]:
                    print(self.formatter.format_success("\nThank you for using Academic RAG System!"))
                    break

                elif command == "help" or command == "?":
                    self.display_help()

                elif command == "history":
                    self.show_history()

                elif command == "clear":
                    self.clear_screen()
                    self.display_welcome()

                elif command == "mode":
                    if args.lower() in ["detailed", "simple"]:
                        generation_mode = args.lower()
                        print(self.formatter.format_success(f"✓ Generation mode set to: {generation_mode}"))
                    else:
                        print(self.formatter.format_error("Invalid mode. Use 'detailed' or 'simple'", "ERROR"))

                elif command == "format":
                    if args.lower() in ["text", "json", "markdown", "summary"]:
                        output_format = args.lower()
                        print(self.formatter.format_success(f"✓ Output format set to: {output_format}"))
                    else:
                        print(self.formatter.format_error("Invalid format. Use 'text', 'json', 'markdown', or 'summary'", "ERROR"))

                elif command == "results":
                    try:
                        n = int(args)
                        if 1 <= n <= 20:
                            num_results = n
                            print(self.formatter.format_success(f"✓ Number of results set to: {num_results}"))
                        else:
                            print(self.formatter.format_error("Number must be between 1 and 20", "ERROR"))
                    except ValueError:
                        print(self.formatter.format_error("Invalid number", "ERROR"))

                elif command == "save":
                    if args:
                        self.save_last_result(args)
                    else:
                        print(self.formatter.format_error("Please specify a filename", "ERROR"))

                elif command == "query":
                    if args:
                        self.run_query(args, num_results, generation_mode, output_format)
                    else:
                        print(self.formatter.format_error("Please provide a query", "ERROR"))

                else:
                    # Treat entire input as a query
                    self.run_query(user_input, num_results, generation_mode, output_format)

            except KeyboardInterrupt:
                print("\n\n" + self.formatter.format_success("Use 'exit' to quit"))
                continue
            except EOFError:
                print("\n")
                break
            except Exception as e:
                print(self.formatter.format_error(f"Unexpected error: {str(e)}", "ERROR"))
                continue


def main():
    """Parse arguments and launch the CLI."""
    parser = argparse.ArgumentParser(
        description="Academic RAG System - Interactive CLI for querying academic papers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (recommended)
  python rag_cli.py

  # Single query
  python rag_cli.py --query "machine learning for classification"

  # Advanced single query
  python rag_cli.py -q "neural networks" -m simple -n 10 -f json

  # Save results
  python rag_cli.py -q "deep learning" -s results.txt

In interactive mode, you can:
  - Type queries directly (no command needed)
  - Change settings on the fly (mode, format, results)
  - View query history
  - Save results to files
        """
    )

    parser.add_argument(
        "--query", "-q",
        type=str,
        help="Run a single query (non-interactive mode)"
    )

    parser.add_argument(
        "--mode", "-m",
        type=str,
        choices=["detailed", "simple"],
        default="detailed",
        help="Generation mode: detailed (default) or simple"
    )

    parser.add_argument(
        "--num-results", "-n",
        type=int,
        default=5,
        help="Number of results to retrieve (default: 5)"
    )

    parser.add_argument(
        "--format", "-f",
        type=str,
        choices=["text", "json", "markdown", "summary"],
        default="text",
        help="Output format (default: text)"
    )

    parser.add_argument(
        "--save", "-s",
        type=str,
        help="Save output to file"
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )

    parser.add_argument(
        "--chroma-path",
        type=str,
        default=None,
        help="Path to Chroma database (default: ./chroma_db)"
    )

    args = parser.parse_args()

    # Setup paths
    base_dir = Path(__file__).parent
    chroma_path = args.chroma_path or str(base_dir / "chroma_db")

    # Verify database exists
    if not Path(chroma_path).exists():
        print(f"Error: Chroma database not found at {chroma_path}")
        print("Please run the data processing and embedding generation first.")
        sys.exit(1)

    # Initialize CLI
    cli = RAGCli(chroma_path=chroma_path, use_colors=not args.no_color)

    # Run in appropriate mode
    if args.query:
        # Single query mode
        result = cli.run_query(
            query=args.query,
            num_results=args.num_results,
            generation_mode=args.mode,
            output_format=args.format
        )

        # Save if requested
        if args.save and result:
            cli.save_last_result(args.save)
    else:
        # Interactive mode
        cli.interactive_mode()


if __name__ == "__main__":
    main()
