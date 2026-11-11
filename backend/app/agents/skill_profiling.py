import os
import json
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from groq import Groq
from ..schemas.student import StudentProfile

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def _normalize_profile_result(result: dict[str, Any]) -> dict[str, Any]:
    graduation_year = result.get("graduation_year")
    if graduation_year == "":
        result["graduation_year"] = None
    elif isinstance(graduation_year, str) and graduation_year.isdigit():
        result["graduation_year"] = int(graduation_year)

    normalized_skills: list[dict[str, Any]] = []
    for raw_skill in result.get("skills") or []:
        if not isinstance(raw_skill, dict):
            continue

        names = raw_skill.get("name") or raw_skill.get("skill") or ""
        if isinstance(names, str):
            skill_names = [name.strip() for name in names.split(",") if name.strip()]
        else:
            skill_names = []

        for name in skill_names:
            normalized_skills.append(
                {
                    "name": name,
                    "category": raw_skill.get("category", ""),
                    "proficiency": raw_skill.get("proficiency", ""),
                    "confidence": raw_skill.get("confidence", 0),
                    "evidence": raw_skill.get("evidence", ""),
                }
            )
    result["skills"] = normalized_skills

    normalized_projects: list[dict[str, Any]] = []
    for raw_project in result.get("projects") or []:
        if not isinstance(raw_project, dict):
            continue
        normalized_projects.append(
            {
                "title": raw_project.get("title") or raw_project.get("name", ""),
                "description": raw_project.get("description", ""),
                "github_url": raw_project.get("github_url") or "",
            }
        )
    result["projects"] = normalized_projects
    return result


def analyze_resume(resume_text: str) -> StudentProfile:

    prompt = f"""
    You are an expert resume analysis assistant.

    Analyze the following student resume.

    Extract:
    1. Full name
    2. University
    3. Degree
    4. Graduation year
    5. Career goal, if explicitly stated
    6. Technical and soft skills
    7. Projects

    For each skill:
    - Give its category.
    - Estimate proficiency as Beginner,
      Intermediate or Advanced.
    - Assign a confidence score between 0 and 1.
    - Include supporting evidence from the resume.

    Never invent qualifications, skills or experience.
    Use null for graduation_year when unavailable. Use empty strings for
    unavailable text fields and empty arrays when there are no skills or projects.
    Every skill must be an object with name, category, proficiency, confidence,
    and evidence. Do not combine multiple skill names in one object.
    Every project must be an object with title, description, and github_url.

    Resume:
    {resume_text}
    """

    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL"),
        messages=[
            {
                "role": "system",
                "content": "Return only valid JSON matching the requested schema."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.1
    )

    result = _normalize_profile_result(
        json.loads(response.choices[0].message.content)
    )

    return StudentProfile.model_validate(result)