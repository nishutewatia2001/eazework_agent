"""Build and format working memory for the EazeHR assistant."""
from __future__ import annotations

from typing import Any, Dict, List

from . import eazework_dummy
from .config import TOP_K
from .faiss_store import PoliciesRetriever
from .memory_db import get_user_memory, init_memory_db


def build_working_memory(
    user_id: str,
    user_query: str,
    retriever: PoliciesRetriever,
    top_k: int = TOP_K,
) -> Dict[str, Any]:
    """Compose a working memory dictionary combining user data, memory, and RAG."""
    init_memory_db()

    user_memory = get_user_memory(user_id)
    summary = eazework_dummy.get_user_summary(user_id)
    active_leaves = eazework_dummy.get_active_leaves(user_id)
    manager_chain = eazework_dummy.get_manager_chain(user_id)
    latest_payslip = eazework_dummy.get_latest_payslip(user_id)

    policy_context = retriever.search(user_query, top_k=top_k)

    return {
        "user": {
            "user_id": user_id,
            "summary": summary,
            "memory": user_memory,
        },
        "query": {"text": user_query},
        "hr_data": {
            "active_leaves": active_leaves,
            "manager_chain": manager_chain,
            "latest_payslip": latest_payslip,
        },
        "policy_context": policy_context,
    }


def format_working_memory_as_prompt(working_memory: Dict[str, Any]) -> str:
    """Create a readable prompt string from the working memory."""
    lines: List[str] = []

    user_section = working_memory.get("user", {})
    lines.append("### USER SUMMARY")
    lines.append(user_section.get("summary") or "No summary available.")
    lines.append("")

    lines.append("### USER MEMORY")
    memory = user_section.get("memory", {}) or {}
    if memory:
        for key, value in memory.items():
            lines.append(f"- {key}: {value}")
    else:
        lines.append("- No stored preferences.")
    lines.append("")

    lines.append("### HR DATA")
    hr_data = working_memory.get("hr_data", {})
    lines.append(f"Active leaves: {hr_data.get('active_leaves')}")
    lines.append(f"Manager chain: {hr_data.get('manager_chain')}")
    lines.append(f"Latest payslip: {hr_data.get('latest_payslip')}")
    lines.append("")

    lines.append("### POLICY CONTEXT (RAG SNIPPETS)")
    policy_context = working_memory.get("policy_context", [])
    if policy_context:
        for item in policy_context:
            lines.append(
                f"- [{item.get('doc_id')} - chunk {item.get('chunk_id')}] "
                f"score={item.get('score'):.4f}"
            )
            lines.append(item.get("text", "").strip())
            lines.append("")
    else:
        lines.append("- No policy snippets found.")
        lines.append("")

    lines.append("### USER QUESTION")
    lines.append(working_memory.get("query", {}).get("text", ""))

    return "\n".join(lines)
