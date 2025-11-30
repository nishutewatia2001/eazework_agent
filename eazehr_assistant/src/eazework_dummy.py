"""A dummy Eazework HR API layer backed by hardcoded demo users."""
from __future__ import annotations

from typing import Dict, Optional

DEMO_USERS: Dict[str, Dict[str, object]] = {
    "U001": {
        "name": "Rohit Sharma",
        "email": "rohit.sharma@example.com",
        "designation": "Senior Data Scientist",
        "department": "GenAI Practice",
        "active_leaves": {"casual": 4, "sick": 6, "earned": 12},
        "manager": "Anurag Gupta",
        "manager_email": "anurag.gupta@example.com",
        "payslip": {
            "month": "2025-10",
            "components": {
                "basic": 60000,
                "hra": 30000,
                "pf": 7200,
                "bonus": 5000,
                "other_allowances": 8000,
            },
        },
        "org_path": "Data Science > GenAI Practice > HR Tech",
    },
    "U002": {
        "name": "Priya Verma",
        "email": "priya.verma@example.com",
        "designation": "ML Engineer",
        "department": "Credit Risk Analytics",
        "active_leaves": {"casual": 2, "sick": 3, "earned": 20},
        "manager": "Piyush Jain",
        "manager_email": "piyush.jain@example.com",
        "payslip": {
            "month": "2025-10",
            "components": {
                "basic": 45000,
                "hra": 22000,
                "pf": 5400,
                "bonus": 3000,
                "other_allowances": 5000,
            },
        },
        "org_path": "Risk & Analytics > Credit Risk > Modelling",
    },
}


def get_active_leaves(user_id: str) -> Optional[Dict[str, int]]:
    user = DEMO_USERS.get(user_id)
    return user.get("active_leaves") if user else None


def get_manager_chain(user_id: str) -> Optional[Dict[str, str]]:
    user = DEMO_USERS.get(user_id)
    if not user:
        return None
    return {
        "manager": user.get("manager"),
        "manager_email": user.get("manager_email"),
        "org_path": user.get("org_path"),
    }


def get_latest_payslip(user_id: str) -> Optional[Dict[str, object]]:
    user = DEMO_USERS.get(user_id)
    return user.get("payslip") if user else None


def get_user_summary(user_id: str) -> Optional[str]:
    user = DEMO_USERS.get(user_id)
    if not user:
        return None
    name = user.get("name", "Unknown")
    designation = user.get("designation", "")
    department = user.get("department", "")
    active_leaves = user.get("active_leaves", {})
    earned = active_leaves.get("earned", 0)
    return (
        f"{name} is a {designation} in {department} with {earned} earned leaves available."
    )
