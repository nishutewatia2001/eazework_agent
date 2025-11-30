"""Utility to ingest policy PDFs, chunk, embed, and store in a FAISS index."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

from .config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_MODEL_NAME,
    FAISS_INDEX_PATH,
    POLICIES_DIR,
    POLICIES_METADATA_PATH,
)


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into overlapping chunks of roughly ``chunk_size`` characters."""
    chunks: List[str] = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end])
        if end == text_length:
            break
        start = max(end - overlap, end) if overlap >= chunk_size else end - overlap
    return [c.strip() for c in chunks if c.strip()]


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from a PDF file using pypdf."""
    reader = PdfReader(str(pdf_path))
    pages_text = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages_text)


def build_index() -> None:
    """Walk the policies directory, chunk, embed, and persist FAISS + metadata."""
    pdf_files = sorted(POLICIES_DIR.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(
            f"No PDFs found in {POLICIES_DIR}. Please add policy PDFs before ingestion."
        )

    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    embeddings: List[np.ndarray] = []
    metadata: List[Dict[str, str | int | float]] = []

    for pdf_path in pdf_files:
        doc_id = pdf_path.stem
        raw_text = extract_text_from_pdf(pdf_path)
        chunks = chunk_text(raw_text)

        if not chunks:
            continue

        chunk_embeddings = model.encode(chunks, convert_to_numpy=True, normalize_embeddings=True)
        for idx, (chunk_text_value, embedding) in enumerate(zip(chunks, chunk_embeddings)):
            embeddings.append(embedding)
            metadata.append(
                {
                    "doc_id": doc_id,
                    "chunk_id": idx,
                    "source_path": str(pdf_path),
                    "text": chunk_text_value,
                }
            )

    if not embeddings:
        raise RuntimeError("No embeddings generated. Ensure PDFs contain extractable text.")

    embeddings_matrix = np.vstack(embeddings).astype("float32")
    dim = embeddings_matrix.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings_matrix)

    FAISS_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(FAISS_INDEX_PATH))
    with POLICIES_METADATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"Built index with {len(metadata)} chunks across {len(pdf_files)} documents.")
    print(f"FAISS index saved to {FAISS_INDEX_PATH}")
    print(f"Metadata saved to {POLICIES_METADATA_PATH}")


def main() -> None:
    build_index()


if __name__ == "__main__":
    main()
