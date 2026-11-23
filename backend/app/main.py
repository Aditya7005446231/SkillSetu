import logging
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware

from .database import get_authenticated_client, get_service_client, supabase
from .services.resume_parser import extract_resume_text
from .services.profile_persistence import save_student_profile
from .services.opportunity_normalizer import normalize_opportunity
from .services.opportunity_sync import sync_opportunities
from .agents.skill_profiling import analyze_resume
from .services.opportunity_sync import sources_from_environment
from .schemas.opportunity import OpportunitySyncRequest
from .services.opportunity_matching import recommend_opportunities

app = FastAPI(title="CareerBridge AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
bearer_scheme = HTTPBearer(auto_error=False)
scheduler = AsyncIOScheduler()
logger = logging.getLogger(__name__)


async def run_scheduled_opportunity_sync():
    sources = sources_from_environment()
    if not sources:
        logger.warning("Opportunity sync skipped: OpenWeb Ninja API key is not configured.")
        return
    try:
        result = await sync_opportunities(get_service_client(), sources)
        logger.info("Scheduled opportunity sync completed: %s", result)
    except Exception:
        logger.exception("Scheduled opportunity sync failed.")


@app.on_event("startup")
async def start_opportunity_scheduler():
    if os.getenv("OPPORTUNITY_SYNC_ENABLED", "false").lower() != "true":
        return
    interval_hours = float(os.getenv("OPPORTUNITY_SYNC_INTERVAL_HOURS", "6"))
    scheduler.add_job(
        run_scheduled_opportunity_sync,
        "interval",
        hours=interval_hours,
        id="opportunity-sync",
        replace_existing=True,
    )
    scheduler.start()


@app.on_event("shutdown")
async def stop_opportunity_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)


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


@app.post("/api/opportunities/sync")
async def sync_opportunity_sources(
    request: OpportunitySyncRequest,
    auth=Depends(get_current_user),
):
    """Fetch, analyze, update, and store configured opportunities."""
    _, authenticated_client = auth
    try:
        return await sync_opportunities(authenticated_client, request.sources)
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Opportunity synchronization failed: {error}",
        ) from error


@app.post("/api/opportunities/sync-local")
async def sync_opportunity_sources_locally(request: Request):
    """Run configured source sync locally without a browser access token."""
    if os.getenv("OPPORTUNITY_SYNC_DEV_MODE", "false").lower() != "true":
        raise HTTPException(status_code=404, detail="Local sync is disabled.")

    client_host = request.client.host if request.client else None
    if client_host not in {"127.0.0.1", "::1", "localhost"}:
        raise HTTPException(status_code=403, detail="Local sync is only available on this machine.")

    sources = sources_from_environment()
    if not sources:
        raise HTTPException(
            status_code=400,
            detail="OPENWEBNINJA_API_KEY is not configured.",
        )

    try:
        return await sync_opportunities(get_service_client(), sources)
    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Local opportunity synchronization failed: {error}",
        ) from error


@app.get("/api/opportunities/recommended")
async def get_recommended_opportunities(
    location: str | None = Query(default=None),
    job_type: str | None = Query(default=None),
    remote: bool = Query(default=False),
    minimum_score: float = Query(default=0, ge=0, le=100),
    limit: int = Query(default=20, ge=1, le=100),
    auth=Depends(get_current_user),
):
    user, authenticated_client = auth
    try:
        recommendations = recommend_opportunities(
            authenticated_client,
            str(user.id),
            location=location,
            job_type=job_type,
            remote=remote,
            minimum_score=minimum_score,
            limit=limit,
        )
        return {
            "success": True,
            "count": len(recommendations),
            "recommendations": [
                recommendation.model_dump()
                for recommendation in recommendations
            ],
        }
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Opportunity matching failed: {error}",
        ) from error


@app.get("/api/opportunities/recommended-local")
async def get_local_recommended_opportunities(
    request: Request,
    location: str | None = Query(default=None),
    job_type: str | None = Query(default=None),
    remote: bool = Query(default=False),
    minimum_score: float = Query(default=0, ge=0, le=100),
    limit: int = Query(default=20, ge=1, le=100),
):
    """Test matching locally with a configured student profile."""
    if os.getenv("OPPORTUNITY_SYNC_DEV_MODE", "false").lower() != "true":
        raise HTTPException(status_code=404, detail="Local matching is disabled.")

    client_host = request.client.host if request.client else None
    if client_host not in {"127.0.0.1", "::1", "localhost"}:
        raise HTTPException(status_code=403, detail="Local matching is only available on this machine.")

    student_id = os.getenv("MATCHING_TEST_STUDENT_ID", "").strip()
    if not student_id:
        raise HTTPException(
            status_code=400,
            detail="Set MATCHING_TEST_STUDENT_ID in backend/.env before testing.",
        )

    try:
        recommendations = recommend_opportunities(
            get_service_client(),
            student_id,
            location=location,
            job_type=job_type,
            remote=remote,
            minimum_score=minimum_score,
            limit=limit,
        )
        return {
            "success": True,
            "student_id": student_id,
            "count": len(recommendations),
            "recommendations": [
                recommendation.model_dump()
                for recommendation in recommendations
            ],
        }
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Local opportunity matching failed: {error}",
        ) from error