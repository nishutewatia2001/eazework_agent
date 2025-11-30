"""Helper utilities for generating embeddings with Google Generative AI."""
from __future__ import annotations

import os
from typing import Iterable, List

import google.generativeai as genai
import numpy as np

from .config import EMBEDDING_MODEL_NAME


def _configure_client() -> None:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GOOGLE_API_KEY environment variable is required for embedding generation."
        )
    genai.configure(api_key=api_key)


def embed_texts(texts: Iterable[str]) -> np.ndarray:
    """Embed a collection of texts using the configured Google embedding model."""
    _configure_client()
    vectors: List[np.ndarray] = []
    for text in texts:
        # google-generativeai returns an object with an ``embedding`` attribute/dict key
        response = genai.embed_content(model=EMBEDDING_MODEL_NAME, content=text)
        embedding = response["embedding"] if isinstance(response, dict) else response.embedding
        vectors.append(np.array(embedding, dtype="float32"))
    return np.vstack(vectors)
