from datetime import datetime, timezone

from supabase import Client

from ..schemas.opportunity import ExtractedOpportunity, RawOpportunity


def save_opportunity(
    client: Client,
    opportunity: RawOpportunity,
    extracted: ExtractedOpportunity | None,
) -> dict:
    """Upsert one job and its standardized skill links."""
    now = datetime.now(timezone.utc).isoformat()
    existing = (
        client.table("jobs")
        .select("id,content_hash")
        .eq("source", opportunity.source)
        .eq("external_id", opportunity.external_id)
        .maybe_single()
        .execute()
    )
    existing_data = existing.data if existing is not None else None

    if existing_data and existing_data.get("content_hash") == opportunity.content_hash:
        client.table("jobs").update(
            {"last_seen_at": now, "is_active": True}
        ).eq("id", existing_data["id"]).execute()
        return {
            "job_id": existing_data["id"],
            "title": opportunity.title,
            "company": opportunity.company,
            "changed": False,
        }

    if extracted is None:
        raise ValueError("Extracted opportunity requirements are required for changed jobs.")

    job_data = {
        "external_id": opportunity.external_id,
        "content_hash": opportunity.content_hash,
        "company": opportunity.company,
        "title": opportunity.title,
        "description": opportunity.description,
        "location": opportunity.location,
        "job_type": opportunity.job_type,
        "apply_url": str(opportunity.apply_url),
        "deadline": opportunity.deadline.isoformat() if opportunity.deadline else None,
        "source": opportunity.source,
        "eligibility": extracted.eligibility.model_dump(),
        "last_seen_at": now,
        "is_active": True,
    }

    if existing_data:
        job_id = existing_data["id"]
        client.table("jobs").update(job_data).eq("id", job_id).execute()
    else:
        inserted = client.table("jobs").insert(job_data).execute()
        if not inserted.data:
            raise RuntimeError("Supabase did not return the inserted job.")
        job_id = inserted.data[0]["id"]

    client.table("job_skills").delete().eq("job_id", job_id).execute()
    for skill in extracted.skills:
        skill_row = (
            client.table("skills")
            .upsert(
                {"name": skill.name, "category": "job requirement"},
                on_conflict="name",
            )
            .select("id")
            .execute()
        )
        if not skill_row.data:
            raise RuntimeError(f"Supabase did not return skill ID for {skill.name}.")

        client.table("job_skills").upsert(
            {
                "job_id": job_id,
                "skill_id": skill_row.data[0]["id"],
                "importance": skill.importance,
            },
            on_conflict="job_id,skill_id",
        ).execute()

    return {
        "job_id": job_id,
        "title": opportunity.title,
        "company": opportunity.company,
        "changed": True,
        "skills": [skill.model_dump() for skill in extracted.skills],
        "eligibility": extracted.eligibility.model_dump(),
    }


def opportunity_changed(client: Client, opportunity: RawOpportunity) -> bool:
    """Return whether a source listing is new or has changed."""
    existing = (
        client.table("jobs")
        .select("id,content_hash")
        .eq("source", opportunity.source)
        .eq("external_id", opportunity.external_id)
        .maybe_single()
        .execute()
    )
    existing_data = existing.data if existing is not None else None
    if not existing_data:
        return True
    return existing_data.get("content_hash") != opportunity.content_hash


def mark_missing_opportunities_inactive(
    client: Client,
    source: str,
    seen_external_ids: list[str],
) -> None:
    """Mark previously active source records missing from the latest sync."""
    active_jobs = (
        client.table("jobs")
        .select("id,external_id")
        .eq("source", source)
        .eq("is_active", True)
        .execute()
    )
    seen = set(seen_external_ids)
    for job in active_jobs.data or []:
        if job.get("external_id") not in seen:
            client.table("jobs").update(
                {"is_active": False}
            ).eq("id", job["id"]).execute()
