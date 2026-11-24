"""Conversational refinement agent that parses natural language into structured student preferences."""

import json
from typing import Any

from ..schemas.preference import PreferenceUpdate
from ..services.llm_validator import call_llm_with_validation
from ..services.skill_framework_rag import normalize_skill


def parse_conversational_preference(
    user_message: str,
    current_preferences: dict[str, Any] | None = None,
) -> PreferenceUpdate:
    """Parse user chat message into structured PreferenceUpdate with 1 validation retry."""
    curr = current_preferences or {}
    curr_summary = {
        "location": curr.get("preferred_location") or "Any",
        "remote_only": bool(curr.get("remote_only", False)),
        "job_type": curr.get("preferred_job_type") or "Any",
        "preferred_skills": curr.get("preferred_skills") or [],
        "target_role": curr.get("target_role") or "Any",
        "minimum_score": curr.get("minimum_score") or 0.0,
    }

    prompt = f"""
You are the SkillSetu AI Career Copilot. The student is conversing with you to refine their job/internship search criteria.

Current Student Preferences:
{json.dumps(curr_summary, indent=2)}

Student Message:
"{user_message}"

Extract the student's requested preference updates and write a brief, warm, motivating assistant reply.

Rules:
1. If the student asks for "remote", "work from home", "wfh", set remote_only = true. If they ask for "onsite" or "in-office", set remote_only = false.
2. If the student specifies a city/country (e.g. Bangalore, Pune, Delhi, Mumbai, Hyderabad), extract it into preferred_location.
3. If the student mentions internships ("intern", "internship"), set preferred_job_type = "internship". If "full-time" or "job", set preferred_job_type = "full-time".
4. If the student specifies skills or technologies (e.g. "React", "Python", "Docker"), extract them into preferred_skills array.
5. If the student mentions a score threshold (e.g. "at least 80%", "minimum 70% match"), extract minimum_score.
6. If the student says "reset" or "clear filters", set location="", remote_only=false, job_type="", minimum_score=0.
7. For any field the student did NOT change or mention, leave it as null (None).
8. Write a clear, concise conversational assistant_message summarizing what filters were adjusted and encouraging the student.
9. Populate filters_applied with clean readable badge strings (e.g. ["Remote Only", "Location: Bangalore"]).

Return JSON matching this exact structure:
{{
  "preferred_location": null,
  "remote_only": null,
  "preferred_job_type": null,
  "preferred_skills": [],
  "target_role": null,
  "minimum_score": null,
  "assistant_message": "...",
  "filters_applied": []
}}
"""

    update = call_llm_with_validation(
        schema=PreferenceUpdate,
        prompt=prompt,
        system_prompt="Return only valid JSON strictly matching the requested PreferenceUpdate schema.",
        temperature=0.1,
        max_retries=1,
    )

    # Canonicalize any extracted preferred skills via RAG
    if update.preferred_skills:
        update.preferred_skills = [
            normalize_skill(skill) for skill in update.preferred_skills if skill.strip()
        ]

    return update
