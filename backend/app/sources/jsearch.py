import httpx
import certifi

from ..config import settings
from ..schemas.opportunity import OpportunitySourceConfig, RawOpportunity

async def fetch_jsearch_jobs(
    config: OpportunitySourceConfig,
) -> list[RawOpportunity]:
    """Fetch jobs from OpenWeb Ninja's JSearch endpoint."""
    if not settings.openwebninja_api_key:
        raise RuntimeError("OPENWEBNINJA_API_KEY is not configured.")

    headers = {
        "x-api-key": settings.openwebninja_api_key,
        "Accept": "application/json",
    }
    params = {
        "query": config.query,
        "country": config.country,
        "num_pages": config.num_pages,
    }

    async with httpx.AsyncClient(
        timeout=30,
        verify=certifi.where(),
    ) as client:
        response = await client.get(
            f"https://{settings.openwebninja_api_host}/jsearch/search-v2",
            headers=headers,
            params=params,
        )
        response.raise_for_status()
        payload = response.json()

    data = payload.get("data", []) if isinstance(payload, dict) else []
    if isinstance(data, dict):
        jobs = data.get("jobs", [])
    else:
        jobs = data
    opportunities = []
    for job in jobs:
        apply_url = job.get("job_apply_link")
        if not apply_url:
            apply_links = job.get("job_apply_links")
            if isinstance(apply_links, list) and apply_links:
                first_link = apply_links[0]
                if isinstance(first_link, dict):
                    apply_url = first_link.get("apply_link")
                elif isinstance(first_link, str):
                    apply_url = first_link
        title = (job.get("job_title") or "").strip()
        description = (job.get("job_description") or "").strip()
        if not title or not description or not apply_url:
            continue

        opportunities.append(
            RawOpportunity(
                external_id=str(job.get("job_id") or apply_url),
                company=(job.get("employer_name") or "Unknown company").strip(),
                title=title,
                description=description,
                location=(job.get("job_location") or "").strip(),
                job_type=(job.get("job_employment_type") or "other").strip(),
                apply_url=apply_url,
                source=config.source_key,
            )
        )
    return opportunities
