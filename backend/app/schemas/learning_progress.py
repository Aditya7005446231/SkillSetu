"""Schemas for student-submitted learning progress and evidence."""

from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator


ProgressStatus = Literal["not_started", "in_progress", "completed"]


class LearningProgressUpdate(BaseModel):
    skill_name: str = Field(min_length=1, max_length=100)
    status: ProgressStatus
    evidence_url: HttpUrl | None = None
    evidence_note: str = Field(default="", max_length=2000)

    @field_validator("skill_name")
    @classmethod
    def strip_skill_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Skill name must not be blank.")
        return value

    @field_validator("evidence_note")
    @classmethod
    def strip_evidence_note(cls, value: str) -> str:
        return value.strip()

    @model_validator(mode="after")
    def require_evidence_for_completion(self):
        if (
            self.status == "completed"
            and self.evidence_url is None
            and len(self.evidence_note) < 20
        ):
            raise ValueError(
                "Provide a project URL or at least 20 characters of evidence "
                "before marking a skill complete."
            )
        return self
