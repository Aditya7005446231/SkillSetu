import os
import json
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from ..schemas.student import StudentProfile

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def analyze_resume(resume_text: str):

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
    Use empty values when information is unavailable.

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

    result = json.loads(
        response.choices[0].message.content
    )

    return StudentProfile.model_validate(result)