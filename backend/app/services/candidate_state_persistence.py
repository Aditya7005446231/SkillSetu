"""Persistence layer for candidate match state and conversational student preferences."""

from datetime import datetime, timezone
import logging
from typing import Any

from supabase import Client

from ..schemas.opportunity import RecommendedOpportunity

logger = logging.getLogger(__name__)

# In-memory cache fallback for development/offline testing
_DEV_MATCHES_CACHE: dict[str, list[dict[str, Any]]] = {}
_DEV_PREFERENCES_CACHE: dict[str, dict[str, Any]] = {}


def save_student_preferences(
    client: Client | None,
    student_id: str,
    preferences: dict[str, Any],
) -> dict[str, Any]:
    """Upsert student filter/search preferences."""
    now = datetime.now(timezone.utc).isoformat()
    record = {
        "student_id": student_id,
        "preferred_location": preferences.get("preferred_location") or "",
        "remote_only": bool(preferences.get("remote_only", False)),
        "preferred_job_type": preferences.get("preferred_job_type") or "",
        "preferred_skills": preferences.get("preferred_skills") or [],
        "target_role": preferences.get("target_role") or "",
        "minimum_score": float(preferences.get("minimum_score") or 0),
        "updated_at": now,
    }

    # Store in dev cache
    _DEV_PREFERENCES_CACHE[student_id] = record

    if client:
        try:
            client.table("student_preferences").upsert(
                record, on_conflict="student_id"
            ).execute()
        except Exception as e:
            logger.warning("Could not persist student_preferences to Supabase: %s", e)

    return record


def get_student_preferences(
    client: Client | None,
    student_id: str,
) -> dict[str, Any]:
    """Fetch current student preferences, falling back to cached defaults."""
    if client:
        try:
            res = (
                client.table("student_preferences")
                .select("*")
                .eq("student_id", student_id)
                .maybe_single()
                .execute()
            )
            if res and res.data:
                _DEV_PREFERENCES_CACHE[student_id] = res.data
                return res.data
        except Exception as e:
            logger.debug("Falling back to in-memory preferences for %s: %s", student_id, e)

    return _DEV_PREFERENCES_CACHE.get(
        student_id,
        {
            "student_id": student_id,
            "preferred_location": "",
            "remote_only": False,
            "preferred_job_type": "",
            "preferred_skills": [],
            "target_role": "",
            "minimum_score": 0.0,
        },
    )


def save_opportunity_matches(
    client: Client | None,
    student_id: str,
    recommendations: list[RecommendedOpportunity],
) -> int:
    """Persist ranked candidate matches so recommendations are persistent and fast to reload."""
    now = datetime.now(timezone.utc).isoformat()
    serialized_rows = []

    for rec in recommendations:
        jid = int(rec.job_id) if str(rec.job_id).isdigit() else rec.job_id
        serialized_rows.append(
            {
                "student_id": student_id,
                "job_id": jid,
                "match_score": rec.match_score,
                "matched_skills": rec.matched_skills,
                "missing_skills": rec.missing_skills,
                "related_gap_skills": rec.related_gap_skills,
                "reason": rec.reason,
                "formula_version": rec.formula_version,
                "calculated_at": now,
            }
        )

    _DEV_MATCHES_CACHE[student_id] = serialized_rows

    if client:
        try:
            if serialized_rows:
                for row in serialized_rows:
                    client.table("opportunity_matches").upsert(
                        row, on_conflict="student_id,job_id"
                    ).execute()
                existing_matches = (
                    client.table("opportunity_matches")
                    .select("job_id")
                    .eq("student_id", student_id)
                    .execute()
                )
                active_job_ids = {
                    str(row["job_id"]) for row in serialized_rows
                }
                for row in existing_matches.data or []:
                    if str(row.get("job_id")) not in active_job_ids:
                        (
                            client.table("opportunity_matches")
                            .delete()
                            .eq("student_id", student_id)
                            .eq("job_id", row["job_id"])
                            .execute()
                        )
            else:
                (
                    client.table("opportunity_matches")
                    .delete()
                    .eq("student_id", student_id)
                    .execute()
                )
        except Exception as e:
            logger.warning("Could not persist opportunity_matches to Supabase: %s", e)

    return len(serialized_rows)


def get_saved_opportunity_matches(
    client: Client | None,
    student_id: str,
    limit: int = 20,
) -> list[dict[str, Any]]:
    """Retrieve precomputed opportunity matches for fast reload upon re-login."""
    if client:
        try:
            res = (
                client.table("opportunity_matches")
                .select("*, jobs(title, company, location, job_type, apply_url)")
                .eq("student_id", student_id)
                .order("match_score", desc=True)
                .limit(limit)
                .execute()
            )
            if res and res.data:
                results = []
                for row in res.data:
                    job_info = row.get("jobs") or {}
                    results.append(
                        {
                            "job_id": str(row.get("job_id")),
                            "title": str(job_info.get("title") or ""),
                            "company": str(job_info.get("company") or ""),
                            "location": str(job_info.get("location") or ""),
                            "job_type": str(job_info.get("job_type") or "other"),
                            "apply_url": str(job_info.get("apply_url") or ""),
                            "match_score": float(row.get("match_score") or 0),
                            "matched_skills": row.get("matched_skills") or [],
                            "missing_skills": row.get("missing_skills") or [],
                            "related_gap_skills": row.get("related_gap_skills") or {},
                            "reason": str(row.get("reason") or ""),
                            "formula_version": str(row.get("formula_version") or ""),
                            "saved_state": True,
                        }
                    )
                return results
        except Exception as e:
            logger.debug("Falling back to in-memory matches for %s: %s", student_id, e)

    return _DEV_MATCHES_CACHE.get(student_id, [])[:limit]
