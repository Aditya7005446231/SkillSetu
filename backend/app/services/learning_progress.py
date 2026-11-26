"""Persistence for per-student learning progress and submitted evidence."""

from datetime import datetime, timezone
from typing import Any

from supabase import Client

from ..schemas.learning_progress import LearningProgressUpdate
from .skill_framework_rag import normalize_skill


def get_student_learning_progress(
    client: Client,
    student_id: str,
) -> list[dict[str, Any]]:
    response = (
        client.table("student_learning_progress")
        .select(
            "skill_key,skill_name,status,evidence_url,evidence_note,updated_at"
        )
        .eq("student_id", student_id)
        .execute()
    )
    return sorted(
        response.data or [],
        key=lambda item: str(item.get("skill_name") or "").casefold(),
    )


def save_student_learning_progress(
    client: Client,
    student_id: str,
    update: LearningProgressUpdate,
) -> dict[str, Any]:
    skill_name = normalize_skill(update.skill_name).strip()
    if not skill_name:
        raise ValueError("Skill name must map to a recognized skill.")

    record = {
        "student_id": student_id,
        "skill_key": skill_name.casefold(),
        "skill_name": skill_name,
        "status": update.status,
        "evidence_url": (
            str(update.evidence_url) if update.evidence_url is not None else None
        ),
        "evidence_note": update.evidence_note,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    response = (
        client.table("student_learning_progress")
        .upsert(record, on_conflict="student_id,skill_key")
        .select(
            "skill_key,skill_name,status,evidence_url,evidence_note,updated_at"
        )
        .execute()
    )
    if not response.data:
        raise RuntimeError("The learning progress update was not persisted.")
    return response.data[0]
