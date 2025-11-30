"""Simple CLI to demonstrate the EazeHR assistant working memory assembly."""
from __future__ import annotations

import argparse

from .faiss_store import PoliciesRetriever
from .working_memory import build_working_memory, format_working_memory_as_prompt


def call_llm(prompt: str) -> str:
    return (
        "This is a fake LLM answer. In a real system we would send the prompt to an LLM API."
    )


def run_cli() -> None:
    parser = argparse.ArgumentParser(description="EazeHR Assistant Demo")
    parser.add_argument("--user_id", required=True, help="User ID (e.g., U001)")
    parser.add_argument("--question", required=True, help="User question")
    args = parser.parse_args()

    retriever = PoliciesRetriever()
    working_memory = build_working_memory(args.user_id, args.question, retriever)
    prompt = format_working_memory_as_prompt(working_memory)

    print("========== ASSEMBLED PROMPT ==========")
    print(prompt)
    print("\n========== FINAL ANSWER ==========")
    print(call_llm(prompt))


def main() -> None:
    run_cli()


if __name__ == "__main__":
    main()
