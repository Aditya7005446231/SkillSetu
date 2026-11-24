from datetime import date
from urllib.parse import quote

from pydantic import BaseModel, Field, HttpUrl


class RawOpportunity(BaseModel):
    external_id: str
    company: str
    title: str
    description: str
    location: str = ""
    job_type: str = "other"
    apply_url: HttpUrl
    deadline: date | None = None
    source: str
    content_hash: str = ""


class ExtractedOpportunity(BaseModel):
    skills: list["RequiredSkill"] = Field(default_factory=list)
    eligibility: "Eligibility" = Field(default_factory=lambda: Eligibility())


class RequiredSkill(BaseModel):
    name: str
    importance: float = Field(default=1, ge=0, le=1)
    is_required: bool = True


class Eligibility(BaseModel):
    degree_requirements: list[str] = Field(default_factory=list)
    graduation_year: int | None = None
    experience_years: int = Field(default=0, ge=0)
    work_authorization: str | None = None
    location_requirements: list[str] = Field(default_factory=list)


class OpportunitySourceConfig(BaseModel):
    source: str = "jsearch"
    query: str = "software developer internship"
    country: str = "in"
    num_pages: int = Field(default=1, ge=1, le=10)

    @property
    def source_key(self) -> str:
        return f"{self.source}:{self.country}:{quote(self.query, safe='')}"


class OpportunitySyncRequest(BaseModel):
    sources: list[OpportunitySourceConfig] = Field(min_length=1)


class RecommendedOpportunity(BaseModel):
    job_id: str
    title: str
    company: str
    location: str = ""
    job_type: str = "other"
    apply_url: str
    match_score: float = Field(ge=0, le=100)
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    related_gap_skills: dict[str, list[str]] = Field(default_factory=dict)
    reason: str
    formula_version: str


class SyncResult(BaseModel):
    fetched: int
    saved: int
    skipped: int
    opportunities: list[dict] = Field(default_factory=list)
