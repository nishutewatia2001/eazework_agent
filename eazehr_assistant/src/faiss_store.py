"""Wrapper around FAISS index and metadata for policy retrieval."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from .config import EMBEDDING_MODEL_NAME, FAISS_INDEX_PATH, POLICIES_METADATA_PATH


class PoliciesRetriever:
    """Lightweight retrieval helper for policy documents."""

    def __init__(
        self,
        index_path: Path = FAISS_INDEX_PATH,
        metadata_path: Path = POLICIES_METADATA_PATH,
        embedding_model_name: str = EMBEDDING_MODEL_NAME,
    ) -> None:
        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)
        self.model = SentenceTransformer(embedding_model_name)
        self.index = faiss.read_index(str(self.index_path))
        self.metadata: List[Dict[str, str | int | float]] = json.loads(
            self.metadata_path.read_text(encoding="utf-8")
        )

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, str | int | float]]:
        """Search the FAISS index and return top_k metadata records with scores."""
        query_embedding = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        query_vector = np.array(query_embedding, dtype="float32")
        scores, indices = self.index.search(query_vector, top_k)

        results: List[Dict[str, str | int | float]] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            metadata = dict(self.metadata[idx])
            metadata["score"] = float(score)
            results.append(metadata)
        return results
