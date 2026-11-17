from html import unescape
import re
from hashlib import sha256

from ..schemas.opportunity import RawOpportunity


def normalize_opportunity(opportunity: RawOpportunity) -> RawOpportunity:
    """Normalize source text before AI extraction and persistence."""
    company = _clean(opportunity.company)
    title = _clean(opportunity.title)
    description = _clean(opportunity.description)
    location = _clean(opportunity.location)
    job_type = _normalize_job_type(opportunity.job_type, title, description)
    searchable_text = f"{title} {description} {location}".lower()

    if "remote" in searchable_text or "work from home" in searchable_text:
        location = f"{location} (Remote)" if location else "Remote"

    content_hash = sha256(
        f"{title}\n{description}\n{location}\n{job_type}".encode("utf-8")
    ).hexdigest()

    return opportunity.model_copy(
        update={
            "company": company,
            "title": title,
            "description": description,
            "location": location,
            "job_type": job_type,
            "content_hash": content_hash,
        }
    )


def _clean(value: str) -> str:
    without_tags = re.sub(r"<[^>]*>", " ", unescape(value or ""))
    return re.sub(r"\s+", " ", without_tags).strip()


def _normalize_job_type(source_type: str, title: str, description: str) -> str:
    searchable_text = f"{source_type} {title} {description}".lower()
    if "intern" in searchable_text:
        return "internship"
    if any(term in searchable_text for term in ("part-time", "part time")):
        return "part-time"
    if "contract" in searchable_text or "freelance" in searchable_text:
        return "contract"
    if any(term in searchable_text for term in ("temporary", "temp ")):
        return "temporary"
    if any(term in searchable_text for term in ("full-time", "full time")):
        return "full-time"
    return "other"
