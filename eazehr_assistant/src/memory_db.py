"""SQLite-backed long-term memory store for user preferences."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Dict

from .config import MEMORY_DB_PATH


SCHEMA = """
CREATE TABLE IF NOT EXISTS user_memory (
  user_id TEXT NOT NULL,
  key TEXT NOT NULL,
  value TEXT NOT NULL,
  last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, key)
);
"""


DEFAULT_MEMORIES = {
    "U001": {"preferred_tone": "simple_friendly", "preferred_language": "english"},
    "U002": {"preferred_tone": "formal", "preferred_language": "english"},
}


def init_memory_db(db_path: Path = MEMORY_DB_PATH) -> None:
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(SCHEMA)
        conn.commit()

    seed_default_memories(db_path)


def seed_default_memories(db_path: Path = MEMORY_DB_PATH) -> None:
    with sqlite3.connect(db_path) as conn:
        for user_id, memories in DEFAULT_MEMORIES.items():
            for key, value in memories.items():
                conn.execute(
                    """
                    INSERT OR REPLACE INTO user_memory (user_id, key, value)
                    VALUES (?, ?, ?)
                    """,
                    (user_id, key, value),
                )
        conn.commit()


def set_user_memory(user_id: str, key: str, value: str, db_path: Path = MEMORY_DB_PATH) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO user_memory (user_id, key, value)
            VALUES (?, ?, ?)
            """,
            (user_id, key, value),
        )
        conn.commit()


def get_user_memory(user_id: str, db_path: Path = MEMORY_DB_PATH) -> Dict[str, str]:
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            "SELECT key, value FROM user_memory WHERE user_id = ?", (user_id,)
        )
        rows = cursor.fetchall()
    return {key: value for key, value in rows}


def main() -> None:
    init_memory_db()
    print(f"Initialized memory DB at {MEMORY_DB_PATH}")


if __name__ == "__main__":
    main()
