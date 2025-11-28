"""Data processing module for extracting and chunking text from PDFs."""

import json
import logging
from pathlib import Path
from typing import List, Dict, Optional
import PyPDF2
import csv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_text_from_pdf(pdf_path: str) -> Optional[str]:
    """
    Extract text from a PDF file.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Extracted text or None if extraction fails
    """
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"Failed to extract text from {pdf_path}: {e}")
        return None


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: Text to chunk
        chunk_size: Number of words per chunk
        overlap: Number of words to overlap between chunks

    Returns:
        List of text chunks
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)

    return chunks


def process_all_pdfs(
    raw_data_dir: str,
    output_dir: str,
    chunk_size: int = 512,
    overlap: int = 50
) -> Dict[str, List[str]]:
    """
    Process all PDFs in a directory, extract text, and create chunks.

    Args:
        raw_data_dir: Directory containing PDF files
        output_dir: Directory to save processed text and metadata
        chunk_size: Words per chunk
        overlap: Word overlap between chunks

    Returns:
        Dictionary mapping PDF filenames to their chunks
    """
    raw_path = Path(raw_data_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    pdf_chunks = {}
    metadata = []

    pdf_files = sorted(raw_path.glob("*.pdf"))
    total_pdfs = len(pdf_files)

    logger.info(f"Found {total_pdfs} PDFs to process")

    for idx, pdf_file in enumerate(pdf_files, 1):
        logger.info(f"Processing {idx}/{total_pdfs}: {pdf_file.name}")

        text = extract_text_from_pdf(str(pdf_file))
        if not text:
            logger.warning(f"Skipped {pdf_file.name} - no text extracted")
            continue

        chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
        pdf_chunks[pdf_file.name] = chunks

        # Save individual file data
        file_data = {
            "filename": pdf_file.name,
            "total_chunks": len(chunks),
            "text_length": len(text),
            "chunks": chunks
        }

        output_file = output_path / f"{pdf_file.stem}_chunks.json"
        with open(output_file, 'w', encoding='utf-8', errors='replace') as f:
            json.dump(file_data, f, ensure_ascii=False, indent=2)

        # Track metadata
        metadata.append({
            "filename": pdf_file.name,
            "total_chunks": len(chunks),
            "text_length": len(text)
        })

    # Save metadata CSV
    metadata_file = output_path / "metadata.csv"
    with open(metadata_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "total_chunks", "text_length"])
        writer.writeheader()
        writer.writerows(metadata)

    logger.info(f"Successfully processed {len(pdf_chunks)}/{total_pdfs} PDFs")
    logger.info(f"Total chunks created: {sum(len(c) for c in pdf_chunks.values())}")
    logger.info(f"Output saved to {output_path}")

    return pdf_chunks


if __name__ == "__main__":
    # Process all PDFs
    raw_dir = Path(__file__).parent.parent / "data" / "raw"
    output_dir = Path(__file__).parent.parent / "data" / "processed"

    chunks = process_all_pdfs(str(raw_dir), str(output_dir))
