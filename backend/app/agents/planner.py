"""Planner Agent: Decomposes high-level user career goals into executable step plans."""

import json
from typing import Any

from ..schemas.agent_plan import AgentPlan
from ..services.llm_validator import call_llm_with_validation


ALLOWED_STEPS_DOC = """
Available Workflow Capabilities:
1. "profile": Analyzes the student's resume or loads their persisted skills, education, and projects.
2. "retrieve": Fetches active relevant job/internship listings from the opportunity database.
3. "match": Matches candidate skills against job requirements, computes match score, identifies gaps and bridge skills.
4. "roadmap": Formulates a step-by-step career milestone roadmap with actionable learning steps to close identified skill gaps.
"""


def generate_agent_plan(
    goal: str,
    context: dict[str, Any] | None = None,
) -> AgentPlan:
    """Use Groq LLM to decompose a goal into an ordered JSON plan using only allowed steps."""
    ctx = context or {}
    has_profile = bool(ctx.get("has_profile", False))
    has_resume_text = bool(ctx.get("has_resume_text", False))

    prompt = f"""
You are the SkillSetu AI Lead Planner Agent.
Your job is to decompose the user's career workflow request into an optimal, ordered sequence of steps.

{ALLOWED_STEPS_DOC}

Current Execution Context:
- User has existing saved profile: {has_profile}
- New resume text provided: {has_resume_text}

User Goal:
"{goal}"

Rules:
1. You may ONLY select steps from: ["profile", "retrieve", "match", "roadmap"].
2. If new resume text is provided or no profile exists, start with "profile".
3. If the user wants job matching, include "retrieve" followed by "match".
4. If the user asks for learning milestones or how to prepare, include "roadmap".
5. For a complete end-to-end request, the standard sequence is: profile -> retrieve -> match -> roadmap.
6. Provide a concise explanation for your reasoning.

Return JSON matching this exact structure:
{{
  "goal": "{goal}",
  "reasoning": "Brief explanation of why this plan was chosen",
  "steps": [
    {{
      "step": "profile",
      "title": "Profile Student Skills",
      "description": "Extract skills from resume",
      "parameters": {{}}
    }}
  ]
}}
"""

    plan = call_llm_with_validation(
        schema=AgentPlan,
        prompt=prompt,
        system_prompt="Return only valid JSON strictly matching the requested AgentPlan schema.",
        temperature=0.0,
        max_retries=1,
    )

    # Sanity filter: ensure only allowed step names exist
    valid_step_names = {"profile", "retrieve", "match", "roadmap"}
    plan.steps = [s for s in plan.steps if s.step in valid_step_names]

    # If empty, fallback to default standard pipeline
    if not plan.steps:
        from ..schemas.agent_plan import PlanStep
        plan.steps = [
            PlanStep(step="profile", title="Profile Candidate", description="Extract candidate skills"),
            PlanStep(step="retrieve", title="Retrieve Opportunities", description="Load active jobs"),
            PlanStep(step="match", title="Match Opportunities", description="Rank opportunities and find gaps"),
            PlanStep(step="roadmap", title="Generate Roadmap", description="Formulate gap closure milestones"),
        ]

    return plan
