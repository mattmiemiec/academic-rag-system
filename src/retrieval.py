"""Retrieval module for semantic search and document ranking."""

import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from .embeddings import EmbeddingManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RetrieverBase:
    """Base class for document retrieval."""

    def __init__(self, chroma_path: str = "./chroma_db"):
        """
        Initialize the retriever.

        Args:
            chroma_path: Path to Chroma database
        """
        self.manager = EmbeddingManager(chroma_path=chroma_path)
        logger.info("Retriever initialized")

    def retrieve(self, query: str, k: int = 5) -> List[Dict]:
        """
        Retrieve documents similar to the query.

        Args:
            query: Query text
            k: Number of results to return

        Returns:
            List of result dictionaries with text, metadata, and distance
        """
        raise NotImplementedError


class SemanticRetriever(RetrieverBase):
    """Semantic search retriever using embeddings."""

    def retrieve(self, query: str, k: int = 5) -> List[Dict]:
        """
        Retrieve documents using semantic similarity.

        Args:
            query: Query text
            k: Number of results to return

        Returns:
            List of result dictionaries with text, metadata, and distance
        """
        logger.info(f"Retrieving {k} documents for query: '{query}'")

        # Query the database
        docs, _, metadatas, distances = self.manager.query(query, k=k)

        # Build result dictionaries
        results = []
        for doc, metadata, distance in zip(docs, metadatas, distances):
            result = {
                "text": doc,
                "source": metadata.get("source", "unknown"),
                "chunk_index": metadata.get("chunk_index", 0),
                "distance": distance,
                "similarity_score": 1 - distance  # Convert distance to similarity
            }
            results.append(result)

        logger.info(f"Retrieved {len(results)} documents")
        return results

    def retrieve_by_source(self, query: str, k: int = 5, unique_sources: bool = True) -> List[Dict]:
        """
        Retrieve documents, optionally filtering for unique sources.

        Args:
            query: Query text
            k: Number of unique sources to return
            unique_sources: If True, return at most one chunk per source document

        Returns:
            List of result dictionaries
        """
        logger.info(f"Retrieving unique sources for query: '{query}'")

        if not unique_sources:
            return self.retrieve(query, k=k)

        # Get more results initially to account for filtering
        initial_k = k * 3
        docs, _, metadatas, distances = self.manager.query(query, k=initial_k)

        # Filter to unique sources
        seen_sources = set()
        results = []

        for doc, metadata, distance in zip(docs, metadatas, distances):
            source = metadata.get("source", "unknown")

            if source not in seen_sources:
                seen_sources.add(source)
                result = {
                    "text": doc,
                    "source": source,
                    "chunk_index": metadata.get("chunk_index", 0),
                    "distance": distance,
                    "similarity_score": 1 - distance
                }
                results.append(result)

                if len(results) >= k:
                    break

        logger.info(f"Retrieved {len(results)} unique sources")
        return results


class HybridRetriever(RetrieverBase):
    """Hybrid retriever combining semantic and keyword search (placeholder)."""

    def retrieve(self, query: str, k: int = 5, semantic_weight: float = 0.7) -> List[Dict]:
        """
        Retrieve documents using hybrid search.

        Args:
            query: Query text
            k: Number of results to return
            semantic_weight: Weight for semantic search (0-1)

        Returns:
            List of result dictionaries
        """
        # For now, this just uses semantic search
        # Future implementation would combine with BM25 or keyword matching
        logger.info(f"Hybrid retrieval for query: '{query}' (semantic weight: {semantic_weight})")

        # Use semantic retriever for now
        docs, _, metadatas, distances = self.manager.query(query, k=k)

        results = []
        for doc, metadata, distance in zip(docs, metadatas, distances):
            result = {
                "text": doc,
                "source": metadata.get("source", "unknown"),
                "chunk_index": metadata.get("chunk_index", 0),
                "distance": distance,
                "similarity_score": 1 - distance
            }
            results.append(result)

        return results


class RankedRetriever(SemanticRetriever):
    """Retriever with result ranking and filtering."""

    def retrieve_and_rank(
        self,
        query: str,
        k: int = 5,
        min_similarity: float = 0.0,
        max_results: int = None
    ) -> List[Dict]:
        """
        Retrieve and rank documents by similarity.

        Args:
            query: Query text
            k: Initial number of results to retrieve
            min_similarity: Minimum similarity score to include
            max_results: Maximum number of results to return

        Returns:
            List of ranked result dictionaries
        """
        logger.info(f"Retrieving and ranking for query: '{query}'")

        # Get initial results
        results = self.retrieve(query, k=k)

        # Filter by minimum similarity
        if min_similarity > 0:
            results = [r for r in results if r["similarity_score"] >= min_similarity]
            logger.info(f"Filtered to {len(results)} results with similarity >= {min_similarity}")

        # Limit results
        if max_results and len(results) > max_results:
            results = results[:max_results]

        return results


def get_retriever(
    retriever_type: str = "semantic",
    chroma_path: str = "./chroma_db"
) -> RetrieverBase:
    """
    Factory function to get a retriever instance.

    Args:
        retriever_type: Type of retriever ("semantic", "hybrid", "ranked")
        chroma_path: Path to Chroma database

    Returns:
        Retriever instance
    """
    retriever_type = retriever_type.lower()

    if retriever_type == "semantic":
        return SemanticRetriever(chroma_path)
    elif retriever_type == "hybrid":
        return HybridRetriever(chroma_path)
    elif retriever_type == "ranked":
        return RankedRetriever(chroma_path)
    else:
        logger.warning(f"Unknown retriever type: {retriever_type}, using semantic")
        return SemanticRetriever(chroma_path)


def main():
    """Test retrieval module."""
    base_dir = Path(__file__).parent.parent
    chroma_path = base_dir / "chroma_db"

    # Test different retriever types
    logger.info("Testing Semantic Retriever")
    logger.info("=" * 50)

    retriever = get_retriever("semantic", str(chroma_path))

    test_queries = [
        "machine learning and artificial intelligence",
        "document analysis and processing",
        "information retrieval systems"
    ]

    for query in test_queries:
        logger.info(f"\nQuery: '{query}'")
        results = retriever.retrieve(query, k=3)

        for idx, result in enumerate(results, 1):
            logger.info(f"\nResult {idx}:")
            logger.info(f"  Source: {result['source']}")
            logger.info(f"  Similarity: {result['similarity_score']:.4f}")
            logger.info(f"  Preview: {result['text'][:150]}...")

    # Test unique source retrieval
    logger.info("\n" + "=" * 50)
    logger.info("Testing Unique Source Retrieval")
    logger.info("=" * 50)

    query = "neural networks and deep learning"
    logger.info(f"\nQuery: '{query}'")
    results = retriever.retrieve_by_source(query, k=3)

    for idx, result in enumerate(results, 1):
        logger.info(f"\nResult {idx}:")
        logger.info(f"  Source: {result['source']}")
        logger.info(f"  Chunk: {result['chunk_index']}")
        logger.info(f"  Similarity: {result['similarity_score']:.4f}")

    # Test ranked retrieval
    logger.info("\n" + "=" * 50)
    logger.info("Testing Ranked Retrieval")
    logger.info("=" * 50)

    retriever_ranked = get_retriever("ranked", str(chroma_path))
    query = "information systems and data management"
    logger.info(f"\nQuery: '{query}'")

    results = retriever_ranked.retrieve_and_rank(
        query,
        k=10,
        min_similarity=0.3,
        max_results=5
    )

    for idx, result in enumerate(results, 1):
        logger.info(f"\nResult {idx}:")
        logger.info(f"  Source: {result['source']}")
        logger.info(f"  Similarity: {result['similarity_score']:.4f}")


if __name__ == "__main__":
    main()
