import re
from typing import Any

from supabase import Client

from ..schemas.opportunity import RecommendedOpportunity
from .candidate_state_persistence import save_opportunity_matches
from .skill_framework_rag import get_related_skills, normalize_skill

FORMULA_VERSION = "coverage-location-type-v2-rag"


def calculate_skill_match(
    student_skills: set[str],
    required_skills: set[str],
) -> tuple[list[str], list[str], float]:
    matched = sorted(student_skills & required_skills)
    missing = sorted(required_skills - student_skills)
    coverage = len(matched) / len(required_skills) if required_skills else 0.0
    return matched, missing, coverage


def location_score(location: str, preferred_location: str | None) -> float:
    if not preferred_location:
        return 1.0
    location_lower = (location or "").lower()
    preference_lower = preferred_location.lower().strip()
    if "remote" in location_lower:
        return 1.0
    if preference_lower in location_lower:
        return 1.0
    return 0.0


def job_type_score(job_type: str, preferred_job_type: str | None) -> float:
    if not preferred_job_type:
        return 1.0
    if (job_type or "").lower() == preferred_job_type.lower().strip():
        return 1.0
    return 0.0


def recommend_opportunities(
    client: Client,
    student_id: str,
    location: str | None = None,
    job_type: str | None = None,
    remote: bool = False,
    minimum_score: float = 0,
    limit: int = 20,
) -> list[RecommendedOpportunity]:
    student_rows = (
        client.table("student_skills")
        .select("skills(name)")
        .eq("student_id", student_id)
        .execute()
    )
    student_skills = {
        normalized
        for row in (student_rows.data or [])
        if (normalized := normalize_skill(_nested_skill_name(row)))
    }

    job_rows = (
        client.table("jobs")
        .select(
            "id,external_id,company,title,location,job_type,apply_url,source,"
            "is_active,last_seen_at"
        )
        .eq("is_active", True)
        .limit(500)
        .execute()
    )
    jobs = job_rows.data or []
    if not jobs:
        return []

    job_skill_rows = (
        client.table("job_skills")
        .select("job_id,importance,skills(name)")
        .in_("job_id", [str(job["id"]) for job in jobs])
        .limit(5000)
        .execute()
    )
    requirements: dict[str, set[str]] = {
        str(job["id"]): set() for job in jobs
    }
    for row in (job_skill_rows.data or []):
        job_id = str(row.get("job_id", ""))
        skill_name = _nested_skill_name(row)
        if job_id in requirements and skill_name:
            requirements[job_id].add(normalize_skill(skill_name))

    recommendations = []
    for job in jobs:
        job_location = str(job.get("location") or "")
        job_job_type = str(job.get("job_type") or "other")
        job_location_lower = job_location.lower()

        if remote and "remote" not in job_location_lower:
            continue
        if location and location.lower().strip() not in job_location_lower:
            continue
        if job_type and job_job_type.lower() != job_type.lower().strip():
            continue

        required_skills = requirements.get(str(job["id"]), set())
        matched, missing, coverage = calculate_skill_match(
            student_skills,
            required_skills,
        )
        loc_score = location_score(job_location, location)
        type_score = job_type_score(job_job_type, job_type)
        match_score = round(
            (0.80 * coverage + 0.10 * loc_score + 0.10 * type_score) * 100,
            1,
        )
        if match_score < minimum_score:
            continue

        gap_bridges = {}
        for missing_s in missing[:3]:
            bridges = get_related_skills(missing_s, limit=3)
            if bridges:
                gap_bridges[missing_s] = bridges

        if matched:
            reason = f"Matched {', '.join(matched)}."
            if missing:
                reason += f" Missing {', '.join(missing)}."
        elif missing:
            reason = f"Missing {', '.join(missing)}."
        else:
            reason = "No extracted job requirements are available."

        recommendations.append(
            RecommendedOpportunity(
                job_id=str(job["id"]),
                title=str(job.get("title") or ""),
                company=str(job.get("company") or ""),
                location=job_location,
                job_type=job_job_type,
                apply_url=str(job.get("apply_url") or ""),
                match_score=match_score,
                matched_skills=matched,
                missing_skills=missing,
                related_gap_skills=gap_bridges,
                reason=reason,
                formula_version=FORMULA_VERSION,
            )
        )

    recommendations.sort(
        key=lambda item: item.match_score,
        reverse=True,
    )
    final_matches = recommendations[:limit]

    # Candidate State: Persist matches so results are saved after each run
    try:
        save_opportunity_matches(client, student_id, final_matches)
    except Exception:
        pass

    return final_matches


def _nested_skill_name(row: dict[str, Any]) -> str:
    skill = row.get("skills")
    if isinstance(skill, dict):
        return str(skill.get("name") or "")
    if isinstance(skill, list) and skill:
        return str(skill[0].get("name") or "")
    return ""
