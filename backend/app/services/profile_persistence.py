from collections.abc import Mapping
from typing import Any

from supabase import Client

from ..schemas.student import StudentProfile


def save_student_profile(
    client: Client,
    user_id: str,
    profile: StudentProfile,
) -> None:
    """Persist an analyzed resume using the authenticated user's ID."""
    client.table("profiles").upsert(
        {
            "id": user_id,
            "full_name": profile.full_name,
            "university": profile.university,
            "degree": profile.degree,
            "graduation_year": profile.graduation_year,
            "career_goal": profile.career_goal,
        },
        on_conflict="id",
    ).execute()

    for skill in profile.skills:
        skill_row = (
            client.table("skills")
            .upsert(
                {"name": skill.name, "category": skill.category},
                on_conflict="name",
            )
            .select("id")
            .execute()
        )
        skill_id = _first_id(skill_row.data, "skill")

        client.table("student_skills").upsert(
            {
                "student_id": user_id,
                "skill_id": skill_id,
                "proficiency": skill.proficiency,
                "confidence": skill.confidence,
                "evidence": skill.evidence,
            },
            on_conflict="student_id,skill_id",
        ).execute()

    for project in profile.projects:
        client.table("projects").insert(
            {
                "student_id": user_id,
                "title": project.title,
                "description": project.description,
                "github_url": project.github_url,
            }
        ).execute()


def _first_id(rows: list[Mapping[str, Any]], resource: str) -> str:
    if not rows or not rows[0].get("id"):
        raise RuntimeError(f"Supabase did not return an ID for the {resource}.")
    return str(rows[0]["id"])
