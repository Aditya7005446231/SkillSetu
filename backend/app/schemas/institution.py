"""Pydantic schemas for the Institutional Placement Cell API."""

from typing import Any
from pydantic import BaseModel, Field


class InstitutionalSkillDemand(BaseModel):
    skill: str
    category: str
    demand_percentage: float = Field(description="Percentage of campus recruiters requiring this skill.")
    openings_count: int = Field(description="Total number of active job openings requiring this skill.")
    yoy_growth: str = Field(description="Year-over-year demand growth percentage.")
    recommended_for_roles: list[str] = Field(default_factory=list)


class InstitutionalDemandResponse(BaseModel):
    is_mock: bool = True
    notice: str = "This is a placeholder mock endpoint simulating campus Training & Placement Cell demand analytics."
    institution_name: str
    placement_season: str
    active_recruiting_partners: int
    total_active_openings: int
    top_demanded_skills: list[InstitutionalSkillDemand]
    role_demand_breakdown: dict[str, float]
    curriculum_gap_recommendations: list[str]
