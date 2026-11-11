from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .database import get_authenticated_client, supabase
from .services.resume_parser import extract_resume_text
from .services.profile_persistence import save_student_profile
from .agents.skill_profiling import analyze_resume

app = FastAPI(title="CareerBridge AI")
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Bearer token required.")

    client = get_authenticated_client(credentials.credentials)
    try:
        response = client.auth.get_user(credentials.credentials)
    except Exception as error:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired authentication token.",
        ) from error

    if response.user is None:
        raise HTTPException(status_code=401, detail="Authenticated user not found.")

    return response.user, client

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
    file: UploadFile = File(...),
    auth=Depends(get_current_user),
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
        user, authenticated_client = auth
        save_student_profile(authenticated_client, str(user.id), profile)

        return {
            "success": True,
            "user_id": str(user.id),
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