"""Generation module for LLM-based relevance explanations."""

import logging
import requests
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExplanationGenerator:
    """Generate relevance explanations using Ollama API."""

    def __init__(self, model: str = "mixtral:8x7b", base_url: str = "http://localhost:11434"):
        """
        Initialize the generator.

        Args:
            model: Ollama model name
            base_url: Ollama API base URL
        """
        self.model = model
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
        logger.info(f"Initialized generator with model: {model}")

    def create_prompt(self, query: str, documents: List[Dict]) -> str:
        """
        Create a prompt combining query and retrieved documents.

        Args:
            query: User's research question
            documents: List of retrieved document dictionaries

        Returns:
            Formatted prompt string
        """
        # Start with the query
        prompt = f"Research Question: {query}\n\n"

        # Add retrieved documents
        prompt += "Retrieved Academic Papers:\n\n"

        for i, doc in enumerate(documents, 1):
            source = doc.get('source', 'unknown')
            similarity = doc.get('similarity_score', 0.0)
            text = doc.get('text', '')

            # Truncate very long documents to keep prompt manageable
            max_length = 500
            if len(text) > max_length:
                text = text[:max_length] + "..."

            prompt += f"--- Paper {i} ---\n"
            prompt += f"Source: {source}\n"
            prompt += f"Similarity Score: {similarity:.3f}\n\n"
            prompt += f"{text}\n\n"

        # Add task instruction
        prompt += "---\n\n"
        prompt += "TASK: Analyze ALL papers above and explain their relevance to the research question.\n\n"
        prompt += "For EACH paper, provide:\n"
        prompt += "- Relevance level: Highly Relevant / Moderately Relevant / Not Relevant\n"
        prompt += "- Explanation: 2-3 sentences based on the content\n"
        prompt += "- Key concepts: List relevant terms from the paper\n\n"
        prompt += "Use this exact format for each paper:\n\n"
        prompt += "[Paper X - filename]\n"
        prompt += "Relevance: [your assessment]\n"
        prompt += "Explanation: [your explanation]\n"
        prompt += "Key Concepts: [comma-separated list]\n\n"
        prompt += "Make sure to analyze ALL papers provided above.\n"

        return prompt

    def generate(self, query: str, documents: List[Dict], system_prompt: str = None) -> str:
        """
        Generate explanation using Ollama API.

        Args:
            query: User's research question
            documents: List of retrieved documents
            system_prompt: Optional system prompt override

        Returns:
            Generated explanation text
        """
        # Default system prompt
        if system_prompt is None:
            system_prompt = (
                "You are an expert research assistant specializing in academic literature. "
                "Your task is to explain why retrieved papers are relevant to a research question. "
                "Base your explanations ONLY on the provided text. "
                "Be specific and cite paper sources. "
                "Use clear, professional language."
            )

        # Create the prompt
        user_prompt = self.create_prompt(query, documents)

        logger.info(f"Generating explanation for query: '{query}'")
        logger.info(f"Prompt length: {len(user_prompt)} characters")

        # Prepare API request
        payload = {
            "model": self.model,
            "prompt": user_prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "num_predict": 2000,  # Allow up to 2000 tokens in response
                "temperature": 0.7     # Some creativity but not too much
            }
        }

        try:
            # Call Ollama API
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()

            result = response.json()
            generated_text = result.get('response', '')

            logger.info(f"Generated explanation ({len(generated_text)} characters)")
            return generated_text

        except requests.exceptions.ConnectionError:
            error_msg = (
                "Could not connect to Ollama. Make sure Ollama is running.\n"
                "Start it with: ollama serve"
            )
            logger.error(error_msg)
            return f"ERROR: {error_msg}"

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return f"ERROR: API request failed - {e}"

    def generate_simple(self, query: str, documents: List[Dict]) -> str:
        """
        Generate a simpler, faster explanation (one sentence per paper).

        Args:
            query: User's research question
            documents: List of retrieved documents

        Returns:
            Generated explanation text
        """
        # Simpler prompt for quick responses
        prompt = f"Research Question: {query}\n\n"
        prompt += "Papers:\n\n"

        for i, doc in enumerate(documents, 1):
            source = doc.get('source', 'unknown')
            text = doc.get('text', '')[:300]  # Shorter excerpts
            prompt += f"{i}. {source}\n{text}...\n\n"

        prompt += "For each paper, write ONE sentence explaining its relevance to the question.\n"
        prompt += "Format: Paper X: [one sentence]"

        system_prompt = "You are a research assistant. Provide brief, accurate relevance assessments."

        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        }

        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get('response', '')
        except Exception as e:
            logger.error(f"Simple generation failed: {e}")
            return f"ERROR: {e}"


def main():
    """Test the generation module."""
    from pathlib import Path
    from .retrieval import get_retriever

    # Setup
    base_dir = Path(__file__).parent.parent
    chroma_path = base_dir / "chroma_db"

    # Initialize retriever and generator
    retriever = get_retriever("semantic", str(chroma_path))
    generator = ExplanationGenerator()

    # Test query
    test_query = "machine learning for document classification"

    print("\n" + "="*60)
    print(f"TEST QUERY: {test_query}")
    print("="*60 + "\n")

    # Retrieve documents
    print("Retrieving relevant documents...")
    documents = retriever.retrieve(test_query, k=3)

    print(f"\nRetrieved {len(documents)} documents:")
    for i, doc in enumerate(documents, 1):
        print(f"  {i}. {doc['source']} (similarity: {doc['similarity_score']:.3f})")

    # Generate explanation
    print("\nGenerating explanation...\n")
    explanation = generator.generate(test_query, documents)

    print("\n" + "="*60)
    print("GENERATED EXPLANATION:")
    print("="*60 + "\n")
    print(explanation)

    print("\n" + "="*60)
    print("\nTesting simple generation...")
    print("="*60 + "\n")

    simple_explanation = generator.generate_simple(test_query, documents)
    print(simple_explanation)


if __name__ == "__main__":
    main()
