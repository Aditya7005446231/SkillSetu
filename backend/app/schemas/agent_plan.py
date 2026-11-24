"""Pydantic schemas for the Planner-Executor agent architecture."""

from typing import Any, Literal
from pydantic import BaseModel, Field


StepType = Literal["profile", "retrieve", "match", "roadmap"]


class PlanStep(BaseModel):
    step: StepType = Field(
        description="The capability step to run: profile, retrieve, match, or roadmap."
    )
    title: str = Field(description="Short human-readable title for this step.")
    description: str = Field(description="Explanation of what this step will accomplish.")
    parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional step execution parameters."
    )


class AgentPlan(BaseModel):
    goal: str = Field(description="The primary objective requested by the user.")
    reasoning: str = Field(description="Why this specific sequence of steps was chosen.")
    steps: list[PlanStep] = Field(
        description="Ordered sequence of steps chosen from profile, retrieve, match, roadmap."
    )


class AgentRunRequest(BaseModel):
    goal: str = Field(
        default="Analyze my profile, match me to top opportunities, and generate my skill gap roadmap.",
        description="Natural language instruction for the planner agent."
    )
    resume_text: str | None = Field(
        default=None,
        description="Optional resume text if profiling a new resume in this run."
    )
    preferences: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional location, job type, or remote preferences."
    )


class AgentRunResponse(BaseModel):
    success: bool = True
    goal: str
    plan: AgentPlan
    execution_trace: list[dict[str, Any]] = Field(default_factory=list)
    profile_summary: dict[str, Any] | None = None
    matches_count: int = 0
    top_matches: list[dict[str, Any]] = Field(default_factory=list)
    roadmap: list[dict[str, Any]] = Field(default_factory=list)
    summary: str = ""
