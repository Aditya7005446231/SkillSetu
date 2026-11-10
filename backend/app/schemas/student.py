from pydantic import BaseModel, Field

class Skill(BaseModel):
    name: str
    category: str
    proficiency: str
    confidence: float = Field(ge=0, le=1)
    evidence: str

class Project(BaseModel):
    title: str
    description: str
    github_url: str = ""

class StudentProfile(BaseModel):
    full_name: str
    university: str = ""
    degree: str = ""
    graduation_year: int | None = None
    career_goal: str = ""
    skills: list[Skill]
    projects: list[Project]