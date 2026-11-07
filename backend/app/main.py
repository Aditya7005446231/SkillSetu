from fastapi import FastAPI

from app.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for SkillSetu.",
)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Return the service health status."""
    return {"status": "ok"}
