import json
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from ..schemas.opportunity import ExtractedOpportunity, RawOpportunity
from ..services.llm_validator import call_llm_with_validation
from ..services.skill_framework_rag import build_framework_context


def extract_opportunity_requirements(
    opportunity: RawOpportunity,
) -> ExtractedOpportunity:
    """Extract skills and eligibility into validated structured data with retry."""
    framework_context = build_framework_context(
        f"{opportunity.title} {opportunity.description}",
        limit=6,
    )
    prompt = f"""
Analyze this job or internship listing. Extract only requirements explicitly
supported by the listing. Do not invent skills, education, dates, or eligibility.

Use the retrieved skill-framework context only to interpret and canonicalize
skill names. Do not add a framework skill unless it is supported by the listing.
Prefer canonical skill names from the framework context.

Retrieved skill-framework context:
{framework_context}

Return JSON with this exact shape:
{{
  "skills": [
    {{"name": "Python", "importance": 0.9, "is_required": true}}
  ],
  "eligibility": {{
    "degree_requirements": [],
    "graduation_year": null,
    "experience_years": 0,
    "work_authorization": null,
    "location_requirements": []
  }}
}}

Title: {opportunity.title}
Location: {opportunity.location}
Description:
{opportunity.description}
"""
    return call_llm_with_validation(
        schema=ExtractedOpportunity,
        prompt=prompt,
        system_prompt="Return only valid JSON matching the requested schema.",
        temperature=0.0,
        max_retries=1,
    )
