"""Output formatting utilities for RAG system results."""

import json
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    @staticmethod
    def disable():
        """Disable colors for non-terminal output."""
        Colors.HEADER = ''
        Colors.BLUE = ''
        Colors.CYAN = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.RED = ''
        Colors.BOLD = ''
        Colors.UNDERLINE = ''
        Colors.END = ''


class OutputFormatter:
    """Format RAG system output for display."""

    def __init__(self, use_colors: bool = True):
        """
        Initialize formatter.

        Args:
            use_colors: Whether to use ANSI colors in output
        """
        self.use_colors = use_colors
        # Create instance-specific color codes
        if use_colors:
            self.HEADER = '\033[95m'
            self.BLUE = '\033[94m'
            self.CYAN = '\033[96m'
            self.GREEN = '\033[92m'
            self.YELLOW = '\033[93m'
            self.RED = '\033[91m'
            self.BOLD = '\033[1m'
            self.UNDERLINE = '\033[4m'
            self.END = '\033[0m'
        else:
            self.HEADER = ''
            self.BLUE = ''
            self.CYAN = ''
            self.GREEN = ''
            self.YELLOW = ''
            self.RED = ''
            self.BOLD = ''
            self.UNDERLINE = ''
            self.END = ''

    def format_header(self, text: str, char: str = "=") -> str:
        """
        Format a header with decorative lines.

        Args:
            text: Header text
            char: Character to use for decoration

        Returns:
            Formatted header string
        """
        line = char * 80
        return f"\n{self.BOLD}{self.BLUE}{line}{self.END}\n{self.BOLD}{text}{self.END}\n{self.BLUE}{line}{self.END}\n"

    def format_subheader(self, text: str) -> str:
        """
        Format a subheader.

        Args:
            text: Subheader text

        Returns:
            Formatted subheader string
        """
        return f"\n{self.BOLD}{self.CYAN}{text}{self.END}\n{'-' * 80}\n"

    def format_query_info(self, query: str, timestamp: Optional[str] = None) -> str:
        """
        Format query information.

        Args:
            query: The search query
            timestamp: Optional timestamp string

        Returns:
            Formatted query information
        """
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        output = self.format_header("SEARCH QUERY")
        output += f"{self.BOLD}Query:{self.END} {query}\n"
        output += f"{self.BOLD}Time:{self.END} {timestamp}\n"
        return output

    def format_retrieval_stats(self, stats: Dict) -> str:
        """
        Format retrieval statistics.

        Args:
            stats: Dictionary with retrieval statistics

        Returns:
            Formatted statistics string
        """
        output = self.format_subheader("RETRIEVAL STATISTICS")

        num_retrieved = stats.get('num_retrieved', 0)
        num_sources = stats.get('num_unique_sources', 0)
        avg_score = stats.get('avg_similarity_score', 0.0)
        retrieval_time = stats.get('retrieval_time_ms', 0)

        output += f"{self.GREEN}✓{self.END} Retrieved: {num_retrieved} chunks from {num_sources} unique papers\n"
        output += f"{self.GREEN}✓{self.END} Average Similarity: {avg_score:.3f}\n"
        output += f"{self.GREEN}✓{self.END} Retrieval Time: {retrieval_time:.2f}ms\n"

        return output

    def format_document(self, doc: Dict, index: int, show_text: bool = True) -> str:
        """
        Format a single retrieved document.

        Args:
            doc: Document dictionary
            index: Document index (1-based)
            show_text: Whether to show document text excerpt

        Returns:
            Formatted document string
        """
        source = doc.get('source', 'unknown')
        similarity = doc.get('similarity_score', 0.0)
        text = doc.get('text', '')

        # Color-code similarity score
        if similarity >= 0.8:
            score_color = self.GREEN
        elif similarity >= 0.6:
            score_color = self.YELLOW
        else:
            score_color = self.RED

        output = f"\n{self.BOLD}[{index}] {source}{self.END}\n"
        output += f"    Similarity: {score_color}{similarity:.3f}{self.END}\n"

        if show_text and text:
            # Show first 200 characters of text
            excerpt = text[:200] + ("..." if len(text) > 200 else "")
            output += f"    Excerpt: {excerpt}\n"

        return output

    def format_documents_list(self, documents: List[Dict], show_text: bool = False) -> str:
        """
        Format a list of retrieved documents.

        Args:
            documents: List of document dictionaries
            show_text: Whether to show text excerpts

        Returns:
            Formatted documents string
        """
        output = self.format_subheader(f"RETRIEVED DOCUMENTS ({len(documents)})")

        for i, doc in enumerate(documents, 1):
            output += self.format_document(doc, i, show_text)

        return output

    def format_explanation(self, explanation: str) -> str:
        """
        Format LLM-generated explanation.

        Args:
            explanation: Generated explanation text

        Returns:
            Formatted explanation string
        """
        output = self.format_subheader("RELEVANCE ANALYSIS")
        output += explanation + "\n"
        return output

    def format_complete_result(
        self,
        query: str,
        documents: List[Dict],
        explanation: str,
        stats: Optional[Dict] = None,
        show_document_text: bool = False
    ) -> str:
        """
        Format complete RAG system output.

        Args:
            query: Search query
            documents: Retrieved documents
            explanation: LLM-generated explanation
            stats: Optional retrieval statistics
            show_document_text: Whether to show document excerpts

        Returns:
            Complete formatted output string
        """
        output = self.format_query_info(query)

        if stats:
            output += self.format_retrieval_stats(stats)

        output += self.format_documents_list(documents, show_document_text)
        output += self.format_explanation(explanation)

        output += self.format_header("END OF RESULTS", char="-")

        return output

    def format_summary(
        self,
        query: str,
        num_documents: int,
        top_sources: List[str],
        key_findings: Optional[str] = None
    ) -> str:
        """
        Format a brief summary of results.

        Args:
            query: Search query
            num_documents: Number of documents retrieved
            top_sources: List of top source names
            key_findings: Optional summary of key findings

        Returns:
            Formatted summary string
        """
        output = self.format_header("SEARCH SUMMARY")
        output += f"{self.BOLD}Query:{self.END} {query}\n"
        output += f"{self.BOLD}Documents Found:{self.END} {num_documents}\n\n"

        output += f"{self.BOLD}Top Sources:{self.END}\n"
        for i, source in enumerate(top_sources[:5], 1):
            output += f"  {i}. {source}\n"

        if key_findings:
            output += f"\n{self.BOLD}Key Findings:{self.END}\n{key_findings}\n"

        return output

    def format_error(self, error_message: str, error_type: str = "ERROR") -> str:
        """
        Format an error message.

        Args:
            error_message: The error message
            error_type: Type of error (ERROR, WARNING, etc.)

        Returns:
            Formatted error string
        """
        return f"\n{self.RED}{self.BOLD}[{error_type}]{self.END} {error_message}\n"

    def format_success(self, message: str) -> str:
        """
        Format a success message.

        Args:
            message: Success message

        Returns:
            Formatted success string
        """
        return f"{self.GREEN}{self.BOLD}✓{self.END} {message}\n"

    def format_progress(self, current: int, total: int, task: str) -> str:
        """
        Format a progress indicator.

        Args:
            current: Current progress
            total: Total items
            task: Task description

        Returns:
            Formatted progress string
        """
        percentage = (current / total * 100) if total > 0 else 0
        bar_length = 40
        filled = int(bar_length * current / total) if total > 0 else 0
        bar = "█" * filled + "░" * (bar_length - filled)

        return f"{self.CYAN}{task}:{self.END} [{bar}] {current}/{total} ({percentage:.1f}%)"

    def format_query_prompt(self, prompt: str) -> str:
        """
        Format an input prompt for the CLI.

        Args:
            prompt: The prompt text to display

        Returns:
            Formatted prompt string
        """
        return f"{self.BOLD}{self.CYAN}{prompt}{self.END} "

    def to_json(
        self,
        query: str,
        documents: List[Dict],
        explanation: str,
        stats: Optional[Dict] = None
    ) -> str:
        """
        Format output as JSON.

        Args:
            query: Search query
            documents: Retrieved documents
            explanation: Generated explanation
            stats: Optional statistics

        Returns:
            JSON string
        """
        output_dict = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "retrieval": {
                "num_documents": len(documents),
                "documents": documents,
                "statistics": stats or {}
            },
            "explanation": explanation
        }

        return json.dumps(output_dict, indent=2, ensure_ascii=False)

    def save_to_file(
        self,
        content: str,
        output_path: Path,
        format_type: str = "txt"
    ) -> bool:
        """
        Save formatted output to file.

        Args:
            content: Content to save
            output_path: Path to output file
            format_type: Format type (txt, json, md)

        Returns:
            True if successful, False otherwise
        """
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True
        except Exception as e:
            print(self.format_error(f"Failed to save output: {e}"))
            return False


class MarkdownFormatter(OutputFormatter):
    """Formatter for Markdown output."""

    def __init__(self):
        """Initialize Markdown formatter (no colors)."""
        super().__init__(use_colors=False)

    def format_header(self, text: str, char: str = "=") -> str:
        """Format header as Markdown."""
        return f"\n# {text}\n\n"

    def format_subheader(self, text: str) -> str:
        """Format subheader as Markdown."""
        return f"\n## {text}\n\n"

    def format_document(self, doc: Dict, index: int, show_text: bool = True) -> str:
        """Format document as Markdown."""
        source = doc.get('source', 'unknown')
        similarity = doc.get('similarity_score', 0.0)
        text = doc.get('text', '')

        output = f"\n### [{index}] {source}\n\n"
        output += f"- **Similarity Score:** {similarity:.3f}\n"

        if show_text and text:
            excerpt = text[:200] + ("..." if len(text) > 200 else "")
            output += f"- **Excerpt:** {excerpt}\n"

        return output

    def format_success(self, message: str) -> str:
        """Format success message in Markdown."""
        return f"✓ {message}\n"

    def format_error(self, error_message: str, error_type: str = "ERROR") -> str:
        """Format error message in Markdown."""
        return f"\n**[{error_type}]** {error_message}\n"


def main():
    """Test the formatter with sample data."""
    # Sample data
    query = "machine learning for document classification"
    documents = [
        {
            "source": "2509.12345.pdf",
            "similarity_score": 0.87,
            "text": "This paper presents a novel approach to document classification using deep learning..."
        },
        {
            "source": "2509.67890.pdf",
            "similarity_score": 0.72,
            "text": "We propose a hybrid method combining traditional machine learning with neural networks..."
        },
        {
            "source": "2509.11111.pdf",
            "similarity_score": 0.65,
            "text": "Text classification has been a fundamental task in natural language processing..."
        }
    ]
    explanation = """
[Paper 1 - 2509.12345.pdf]
Relevance: Highly Relevant
Explanation: This paper directly addresses the query by presenting novel deep learning approaches for document classification. The methodology and results are closely aligned with machine learning techniques.
Key Concepts: document classification, deep learning, neural networks, feature extraction

[Paper 2 - 2509.67890.pdf]
Relevance: Moderately Relevant
Explanation: The hybrid approach combining traditional ML with neural networks offers relevant insights for document classification tasks, though not as focused as Paper 1.
Key Concepts: hybrid methods, machine learning, neural networks, classification

[Paper 3 - 2509.11111.pdf]
Relevance: Moderately Relevant
Explanation: Provides foundational context for text classification in NLP, which is relevant background for document classification approaches.
Key Concepts: text classification, NLP, natural language processing
"""

    stats = {
        "num_retrieved": 3,
        "num_unique_sources": 3,
        "avg_similarity_score": 0.747,
        "retrieval_time_ms": 42.5
    }

    # Test colored terminal output
    print("\n" + "="*80)
    print("TESTING COLORED TERMINAL OUTPUT")
    print("="*80)

    formatter = OutputFormatter(use_colors=True)
    output = formatter.format_complete_result(
        query=query,
        documents=documents,
        explanation=explanation,
        stats=stats,
        show_document_text=True
    )
    print(output)

    # Test summary format
    print("\n" + "="*80)
    print("TESTING SUMMARY FORMAT")
    print("="*80)

    summary = formatter.format_summary(
        query=query,
        num_documents=len(documents),
        top_sources=[doc['source'] for doc in documents],
        key_findings="Strong focus on deep learning and hybrid approaches for classification tasks."
    )
    print(summary)

    # Test JSON format
    print("\n" + "="*80)
    print("TESTING JSON FORMAT")
    print("="*80)

    json_output = formatter.to_json(query, documents, explanation, stats)
    print(json_output)

    # Test Markdown format
    print("\n" + "="*80)
    print("TESTING MARKDOWN FORMAT")
    print("="*80)

    md_formatter = MarkdownFormatter()
    md_output = md_formatter.format_complete_result(
        query=query,
        documents=documents,
        explanation=explanation,
        stats=stats,
        show_document_text=True
    )
    print(md_output)

    # Test progress indicator
    print("\n" + "="*80)
    print("TESTING PROGRESS INDICATOR")
    print("="*80)

    for i in range(0, 101, 10):
        print(f"\r{formatter.format_progress(i, 100, 'Processing documents')}", end='', flush=True)
    print()  # New line after progress complete


if __name__ == "__main__":
    main()
