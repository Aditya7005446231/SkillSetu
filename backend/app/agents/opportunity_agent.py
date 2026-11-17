import json
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from ..schemas.opportunity import ExtractedOpportunity, RawOpportunity

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_opportunity_requirements(
    opportunity: RawOpportunity,
) -> ExtractedOpportunity:
    """Extract skills and eligibility into validated structured data."""
    prompt = f"""
Analyze this job or internship listing. Extract only requirements explicitly
supported by the listing. Do not invent skills, education, dates, or eligibility.

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
    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL"),
        messages=[
            {"role": "system", "content": "Return only valid JSON."},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    result = json.loads(response.choices[0].message.content)
    return ExtractedOpportunity.model_validate(result)
