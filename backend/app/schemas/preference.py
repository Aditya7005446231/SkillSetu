"""Pydantic schemas for student conversational preferences and chat interactions."""

from typing import Any
from pydantic import BaseModel, Field

from .opportunity import RecommendedOpportunity


class PreferenceUpdate(BaseModel):
    """Structured preference delta extracted from natural language chat messages."""
    preferred_location: str | None = Field(
        default=None,
        description="Location name mentioned by user (e.g. Bangalore, Mumbai, Delhi, or empty for anywhere)."
    )
    remote_only: bool | None = Field(
        default=None,
        description="True if the user requested remote/work-from-home only, False if onsite, None if unchanged."
    )
    preferred_job_type: str | None = Field(
        default=None,
        description="Job type (internship, full-time, contract, part-time), or None if unspecified."
    )
    preferred_skills: list[str] = Field(
        default_factory=list,
        description="Specific skills or tech stack user wants to focus on."
    )
    target_role: str | None = Field(
        default=None,
        description="Target job title or role (e.g. Frontend Developer, AI Engineer)."
    )
    minimum_score: float | None = Field(
        default=None,
        ge=0,
        le=100,
        description="Minimum match percentage threshold requested by student."
    )
    assistant_message: str = Field(
        default="I have updated your preferences and refreshed your recommendations.",
        description="Conversational, friendly response acknowledging the student's request."
    )
    filters_applied: list[str] = Field(
        default_factory=list,
        description="Human-readable badges of filters applied (e.g. ['Remote Only', 'Location: Bangalore'])."
    )


class ChatMessageRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)


class ChatMessageResponse(BaseModel):
    success: bool = True
    user_message: str
    reply: str
    filters_applied: list[str] = Field(default_factory=list)
    preferences: dict[str, Any] = Field(default_factory=dict)
    count: int = 0
    recommendations: list[RecommendedOpportunity] = Field(default_factory=list)
