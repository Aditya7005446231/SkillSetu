from fastapi import FastAPI, HTTPException
from app.database import supabase
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for SkillSetu.",
)


@app.get("/")
def home():
    return {"message": "Welcome to the SkillSetu API!"}


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Return the service health status."""
    return {"status": "ok"}

@app.get("/db-test")
def test_database_connection():
    try:
        response = supabase.table("skills").select("*").limit(5).execute()

        return{
            "status": "connected",
            "message": "Successfully connected to the database.",
            "data": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
