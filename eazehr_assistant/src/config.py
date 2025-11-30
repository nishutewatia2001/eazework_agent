"""Configuration constants for the EazeHR assistant demo."""
from pathlib import Path

POLICIES_DIR = Path("data/policies")
FAISS_INDEX_PATH = Path("data/faiss_policies.index")
POLICIES_METADATA_PATH = Path("data/policies_metadata.json")
MEMORY_DB_PATH = Path("data/memory.db")
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
TOP_K = 5

# Ensure expected directories exist
POLICIES_DIR.mkdir(parents=True, exist_ok=True)
MEMORY_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
