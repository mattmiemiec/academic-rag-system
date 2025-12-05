#!/usr/bin/env python3
"""
Demo script showing different output formatting options for the RAG system.

Usage:
    python demo_formatting.py --query "your search query" --format [text|json|markdown|summary]
    python demo_formatting.py --query "machine learning" --save outputs/result.txt
"""

import argparse
from pathlib import Path
from src.retrieval import get_retriever
from src.generation import ExplanationGenerator
from src.output_formatter import OutputFormatter, MarkdownFormatter


def run_query(
    query: str,
    output_format: str = "text",
    save_path: str = None,
    num_results: int = 5,
    show_excerpts: bool = True,
    use_colors: bool = True
):
    """
    Run a query and display results in the specified format.

    Args:
        query: Search query
        output_format: Output format (text, json, markdown, summary)
        save_path: Optional path to save output
        num_results: Number of results to retrieve
        show_excerpts: Whether to show document excerpts
        use_colors: Whether to use colored terminal output
    """
    # Setup paths
    base_dir = Path(__file__).parent
    chroma_path = base_dir / "chroma_db"

    # Initialize components
    print("Initializing RAG system...")
    retriever = get_retriever("semantic", str(chroma_path))
    generator = ExplanationGenerator()

    # Choose formatter based on output format
    if output_format == "markdown":
        formatter = MarkdownFormatter()
    else:
        formatter = OutputFormatter(use_colors=use_colors)

    # Display query
    print(formatter.format_query_info(query))

    # Retrieve documents
    print(formatter.format_progress(0, 100, "Retrieving documents"))
    documents, stats = retriever.retrieve_with_stats(query, k=num_results)
    print(f"\r{formatter.format_progress(100, 100, 'Retrieving documents')}")

    if not documents:
        print(formatter.format_error("No documents found for query", "WARNING"))
        return

    print(formatter.format_retrieval_stats(stats))

    # Generate explanation
    print(formatter.format_progress(0, 100, "Generating explanation"))
    explanation = generator.generate(query, documents)
    print(f"\r{formatter.format_progress(100, 100, 'Generating explanation')}\n")

    # Format output based on requested format
    if output_format == "json":
        output = formatter.to_json(query, documents, explanation, stats)
    elif output_format == "summary":
        top_sources = [doc['source'] for doc in documents[:5]]
        # Extract a brief key finding from the explanation
        key_finding = explanation.split('\n')[0] if explanation else "See analysis below"
        output = formatter.format_summary(
            query=query,
            num_documents=len(documents),
            top_sources=top_sources,
            key_findings=key_finding
        )
    else:  # text or markdown
        output = formatter.format_complete_result(
            query=query,
            documents=documents,
            explanation=explanation,
            stats=stats,
            show_document_text=show_excerpts
        )

    # Display output
    print(output)

    # Save if requested
    if save_path:
        save_file = Path(save_path)
        if formatter.save_to_file(output, save_file, output_format):
            print(formatter.format_success(f"Output saved to {save_file}"))
        else:
            print(formatter.format_error(f"Failed to save output to {save_file}"))


def main():
    """Parse arguments and run demo."""
    parser = argparse.ArgumentParser(
        description="Demo of RAG system output formatting options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic query with colored output
  python demo_formatting.py --query "machine learning for classification"

  # JSON output
  python demo_formatting.py --query "neural networks" --format json

  # Save to file
  python demo_formatting.py --query "NLP techniques" --save outputs/nlp_results.txt

  # Summary view with more results
  python demo_formatting.py --query "deep learning" --format summary --num-results 10

  # Markdown format without colors
  python demo_formatting.py --query "AI ethics" --format markdown --no-color
        """
    )

    parser.add_argument(
        "--query", "-q",
        type=str,
        required=True,
        help="Search query"
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
        "--num-results", "-n",
        type=int,
        default=5,
        help="Number of results to retrieve (default: 5)"
    )

    parser.add_argument(
        "--no-excerpts",
        action="store_true",
        help="Don't show document excerpts"
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )

    args = parser.parse_args()

    # Run the query
    run_query(
        query=args.query,
        output_format=args.format,
        save_path=args.save,
        num_results=args.num_results,
        show_excerpts=not args.no_excerpts,
        use_colors=not args.no_color
    )


if __name__ == "__main__":
    main()
