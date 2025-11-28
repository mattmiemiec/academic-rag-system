"""Embeddings module for generating and storing vector embeddings."""

import json
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingManager:
    """Manage embeddings and vector database operations."""

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        chroma_path: str = "./chroma_db",
        collection_name: str = "academic_papers"
    ):
        """
        Initialize the embedding manager.

        Args:
            model_name: Name of the sentence-transformers model
            chroma_path: Path to persistent Chroma database
            collection_name: Name of the collection in Chroma
        """
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.embedding_dim = self.model.get_sentence_embedding_dimension()

        logger.info(f"Initializing Chroma client at {chroma_path}")
        self.client = chromadb.PersistentClient(
            path=chroma_path,
            settings=Settings(anonymized_telemetry=False)
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        self.collection_name = collection_name

        logger.info(f"Embedding dimension: {self.embedding_dim}")

    def load_chunks_from_directory(
        self,
        processed_data_dir: str
    ) -> Tuple[List[str], List[Dict], List[str]]:
        """
        Load all chunks from processed data directory.

        Args:
            processed_data_dir: Path to directory with processed chunk JSON files

        Returns:
            Tuple of (chunk_texts, metadata_list, chunk_ids)
        """
        processed_path = Path(processed_data_dir)
        chunk_texts = []
        metadata_list = []
        chunk_ids = []

        json_files = sorted(processed_path.glob("*_chunks.json"))
        logger.info(f"Found {len(json_files)} chunk files to load")

        chunk_counter = 0
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                filename = data.get("filename", json_file.stem)
                chunks = data.get("chunks", [])

                for chunk_idx, chunk in enumerate(chunks):
                    chunk_id = f"{json_file.stem}_chunk_{chunk_idx}"
                    chunk_texts.append(chunk)
                    chunk_ids.append(chunk_id)
                    metadata_list.append({
                        "source": filename,
                        "chunk_index": chunk_idx,
                        "chunk_count": len(chunks)
                    })
                    chunk_counter += 1

            except Exception as e:
                logger.error(f"Failed to load {json_file}: {e}")
                continue

        logger.info(f"Loaded {chunk_counter} total chunks from {len(json_files)} files")
        return chunk_texts, metadata_list, chunk_ids

    def generate_embeddings(
        self,
        texts: List[str],
        batch_size: int = 100,
        show_progress: bool = True
    ) -> np.ndarray:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of text strings to embed
            batch_size: Batch size for processing
            show_progress: Whether to show progress information

        Returns:
            NumPy array of embeddings
        """
        if show_progress:
            logger.info(f"Generating embeddings for {len(texts)} texts (batch size: {batch_size})")

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress
        )

        logger.info(f"Generated embeddings shape: {embeddings.shape}")
        return embeddings

    def store_embeddings(
        self,
        chunk_ids: List[str],
        chunk_texts: List[str],
        embeddings: np.ndarray,
        metadata_list: List[Dict],
        batch_size: int = 100
    ) -> None:
        """
        Store embeddings in Chroma database.

        Args:
            chunk_ids: List of unique chunk IDs
            chunk_texts: List of chunk texts
            embeddings: NumPy array of embeddings
            metadata_list: List of metadata dictionaries
            batch_size: Batch size for insertion
        """
        logger.info(f"Storing {len(chunk_ids)} embeddings in Chroma database")

        # Process in batches
        for i in range(0, len(chunk_ids), batch_size):
            batch_end = min(i + batch_size, len(chunk_ids))
            batch_ids = chunk_ids[i:batch_end]
            batch_texts = chunk_texts[i:batch_end]
            batch_embeddings = embeddings[i:batch_end]
            batch_metadata = metadata_list[i:batch_end]

            self.collection.add(
                ids=batch_ids,
                documents=batch_texts,
                embeddings=batch_embeddings.tolist(),
                metadatas=batch_metadata
            )

            if (i // batch_size + 1) % 10 == 0:
                logger.info(f"Stored {batch_end}/{len(chunk_ids)} embeddings")

        logger.info(f"Successfully stored all {len(chunk_ids)} embeddings")

    def query(
        self,
        query_text: str,
        k: int = 5
    ) -> Tuple[List[str], List[List[float]], List[Dict], List[float]]:
        """
        Query the vector database for similar chunks.

        Args:
            query_text: Query text to search for
            k: Number of results to return

        Returns:
            Tuple of (chunk_texts, embeddings, metadata, distances)
        """
        # Generate query embedding
        query_embedding = self.model.encode(query_text)

        # Query the collection
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=k
        )

        # Extract results
        ids = results['ids'][0] if results['ids'] else []
        documents = results['documents'][0] if results['documents'] else []
        metadatas = results['metadatas'][0] if results['metadatas'] else []
        distances = results['distances'][0] if results['distances'] else []

        return documents, None, metadatas, distances

    def get_collection_stats(self) -> Dict:
        """Get statistics about the stored collection."""
        count = self.collection.count()
        return {
            "collection_name": self.collection_name,
            "total_documents": count,
            "embedding_model": self.model_name,
            "embedding_dimension": self.embedding_dim
        }


def main():
    """Main function to generate and store embeddings."""
    # Paths
    base_dir = Path(__file__).parent.parent
    processed_data_dir = base_dir / "data" / "processed"
    chroma_path = base_dir / "chroma_db"

    # Initialize manager
    manager = EmbeddingManager(chroma_path=str(chroma_path))

    # Load chunks
    logger.info("Loading chunks from processed data...")
    chunk_texts, metadata_list, chunk_ids = manager.load_chunks_from_directory(
        str(processed_data_dir)
    )

    logger.info(f"Loaded {len(chunk_texts)} chunks")

    # Generate embeddings
    logger.info("Generating embeddings...")
    embeddings = manager.generate_embeddings(chunk_texts, batch_size=100)

    # Store embeddings
    logger.info("Storing embeddings in database...")
    manager.store_embeddings(chunk_ids, chunk_texts, embeddings, metadata_list)

    # Get stats
    stats = manager.get_collection_stats()
    logger.info(f"Collection stats: {stats}")

    # Test query
    logger.info("\n" + "="*50)
    logger.info("Testing semantic search with sample query")
    logger.info("="*50)

    test_queries = [
        "machine learning algorithms",
        "natural language processing",
        "deep neural networks"
    ]

    for query in test_queries:
        logger.info(f"\nQuery: '{query}'")
        docs, _, metadatas, distances = manager.query(query, k=3)

        for idx, (doc, metadata, distance) in enumerate(zip(docs, metadatas, distances)):
            logger.info(f"\n  Result {idx + 1} (distance: {distance:.4f})")
            logger.info(f"  Source: {metadata.get('source')}")
            logger.info(f"  Preview: {doc[:200]}...")


if __name__ == "__main__":
    main()
