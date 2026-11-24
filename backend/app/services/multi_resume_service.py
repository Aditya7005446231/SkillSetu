"""
Service for managing multiple resumes, active resume switching, and manual profile creation.
Maintains Supabase persistence with in-memory dev cache fallback.
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any
from supabase import Client

from ..schemas.student import StudentProfile

logger = logging.getLogger(__name__)

# In-memory dev cache: student_id -> list of resume dicts
_DEV_RESUMES_CACHE: dict[str, list[dict[str, Any]]] = {}


def list_student_resumes(client: Client, student_id: str) -> list[dict[str, Any]]:
    """Return all resumes for a student."""
    try:
        response = (
            client.table("student_resumes")
            .select("*")
            .eq("student_id", student_id)
            .order("created_at", desc=False)
            .execute()
        )
        if response.data:
            return response.data
    except Exception as exc:
        logger.warning(f"Could not read student_resumes from Supabase ({exc}). Using dev cache.")

    return _DEV_RESUMES_CACHE.get(student_id, [])


def save_student_resume(
    client: Client,
    student_id: str,
    label: str,
    filename: str,
    profile: StudentProfile,
    target_role: str = "",
    career_goal: str = "",
    make_active: bool = True,
    resume_id: str | None = None,
) -> dict[str, Any]:
    """
    Save a new or updated resume profile.
    If make_active is True, marks all other resumes for this student as inactive.
    """
    res_id = resume_id or str(uuid.uuid4())
    now_iso = datetime.now(timezone.utc).isoformat()

    record = {
        "id": res_id,
        "student_id": student_id,
        "label": label or "Primary Resume",
        "filename": filename or "profile.pdf",
        "career_goal": career_goal or profile.career_goal or "",
        "target_role": target_role or profile.career_goal or "",
        "is_active": make_active,
        "parsed_profile": profile.model_dump(),
        "created_at": now_iso,
        "updated_at": now_iso,
    }

    # Update in-memory dev cache
    cached = _DEV_RESUMES_CACHE.setdefault(student_id, [])
    if make_active:
        for r in cached:
            r["is_active"] = False

    existing_idx = next((i for i, r in enumerate(cached) if r["id"] == res_id), None)
    if existing_idx is not None:
        cached[existing_idx] = record
    else:
        cached.append(record)

    # Attempt Supabase write
    try:
        if make_active:
            # Set other resumes to inactive
            (
                client.table("student_resumes")
                .update({"is_active": False})
                .eq("student_id", student_id)
                .execute()
            )

        client.table("student_resumes").upsert(
            record,
            on_conflict="id",
        ).execute()
    except Exception as exc:
        logger.warning(f"Could not persist resume to Supabase ({exc}). Kept in dev cache.")

    return record


def set_active_resume(client: Client, student_id: str, resume_id: str) -> dict[str, Any] | None:
    """Set the active resume for a student and return it."""
    # In-memory update
    cached = _DEV_RESUMES_CACHE.get(student_id, [])
    active_item = None
    for r in cached:
        if r["id"] == resume_id:
            r["is_active"] = True
            active_item = r
        else:
            r["is_active"] = False

    # Supabase update
    try:
        (
            client.table("student_resumes")
            .update({"is_active": False})
            .eq("student_id", student_id)
            .execute()
        )
        resp = (
            client.table("student_resumes")
            .update({"is_active": True})
            .eq("student_id", student_id)
            .eq("id", resume_id)
            .execute()
        )
        if resp.data:
            return resp.data[0]
    except Exception as exc:
        logger.warning(f"Could not update active resume in Supabase ({exc}).")

    return active_item


def get_active_resume_profile(client: Client, student_id: str) -> dict[str, Any] | None:
    """Retrieve the currently active resume/profile for matching."""
    try:
        resp = (
            client.table("student_resumes")
            .select("*")
            .eq("student_id", student_id)
            .eq("is_active", True)
            .limit(1)
            .execute()
        )
        if resp.data:
            return resp.data[0]
    except Exception:
        pass

    cached = _DEV_RESUMES_CACHE.get(student_id, [])
    for r in cached:
        if r.get("is_active"):
            return r
    if cached:
        return cached[0]
    return None
