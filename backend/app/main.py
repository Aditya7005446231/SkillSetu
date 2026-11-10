from fastapi import FastAPI, UploadFile, File, HTTPException

from .database import supabase
from .services.resume_parser import extract_resume_text
from .agents.skill_profiling import analyze_resume

app = FastAPI(title="CareerBridge AI")

@app.get("/")
def home():
    return {"message": "CareerBridge AI running"}

@app.get("/db-test")
def test_database_connection():
    response = supabase.table("skills").select("*").limit(5).execute()

    return {
        "status": "connected",
        "message": "Successfully connected to the database.",
        "data": response.data,
    }

@app.post("/api/resume/analyze")
async def analyze_student_resume(
    file: UploadFile = File(...)
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported"
        )

    try:
        file_bytes = await file.read()

        if len(file_bytes) > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail="Resume must be smaller than 5 MB"
            )

        resume_text = extract_resume_text(file_bytes)

        profile = analyze_resume(resume_text)

        return {
            "success": True,
            "profile": profile.model_dump()
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        await file.close()