import logging
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware

from .database import get_authenticated_client, get_service_client, supabase
from .services.resume_parser import extract_resume_text
from .services.profile_persistence import (
    replace_student_skills,
    save_student_profile,
)
from .services.opportunity_normalizer import normalize_opportunity
from .services.opportunity_sync import sync_opportunities
from .agents.skill_profiling import analyze_resume
from .agents.chat_agent import parse_conversational_preference
from .agents.planner import generate_agent_plan
from .agents.executor import AgentState, execute_plan
from .services.opportunity_sync import sources_from_environment
from .schemas.opportunity import OpportunitySyncRequest
from .schemas.preference import ChatMessageRequest, ChatMessageResponse
from .schemas.agent_plan import AgentRunRequest, AgentRunResponse
from .schemas.institution import InstitutionalDemandResponse, InstitutionalSkillDemand
from .schemas.learning_progress import LearningProgressUpdate
from .schemas.student import Skill
from .services.opportunity_matching import recommend_opportunities
from .services.candidate_state_persistence import (
    get_student_preferences,
    save_student_preferences,
    get_saved_opportunity_matches,
)
from .services.learning_roadmap import build_learning_roadmaps
from .services.learning_progress import (
    get_student_learning_progress,
    save_student_learning_progress,
)
from .services.multi_resume_service import (
    list_student_resumes,
    save_student_resume,
    set_active_resume,
    get_active_resume_profile,
)
from .services.skill_framework_rag import (
    get_framework_engine,
    get_related_skills,
    normalize_skill,
    search_skill_framework,
)

app = FastAPI(title="SkillSetu AI")
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
    return {"message": "SkillSetu AI running"}


@app.get("/health")
def health_check():
    """Health check endpoint for container and deployment readiness."""
    return {"status": "ok", "service": "SkillSetu API"}


@app.get("/api/skill-framework/search")
def search_skill_framework_endpoint(
    query: str = Query(min_length=2),
    limit: int = Query(default=5, ge=1, le=20),
):
    """Search the versioned SkillSetu skill-framework knowledge base."""
    return search_skill_framework(query, limit)


@app.get("/api/skill-framework/normalize")
def normalize_skill_endpoint(
    skill: str = Query(min_length=1),
):
    """Normalize raw or aliased skill into canonical framework name."""
    canonical = normalize_skill(skill)
    return {
        "raw": skill,
        "canonical": canonical,
        "is_normalized": canonical.lower() != skill.lower().strip(),
    }


@app.get("/api/skill-framework/gaps")
def get_skill_gaps_endpoint(
    skill: str = Query(min_length=1),
    limit: int = Query(default=4, ge=1, le=10),
):
    """Fetch related skills and prerequisites for bridging a missing skill gap."""
    canonical = normalize_skill(skill)
    related = get_related_skills(skill, limit=limit)
    return {
        "skill": skill,
        "canonical": canonical,
        "related_bridging_skills": related,
    }


@app.get("/api/institution/skills", response_model=InstitutionalDemandResponse)
def get_institutional_skill_demand(
    category: str | None = Query(default=None, description="Optional category filter (e.g. 'Frontend', 'AI')"),
):
    """Mock Training & Placement Cell institutional skill demand analytics API."""
    skills_data = [
        InstitutionalSkillDemand(
            skill="Data Structures & Algorithms",
            category="Computer Science Core",
            demand_percentage=92.0,
            openings_count=160,
            yoy_growth="+5%",
            recommended_for_roles=["Software Engineer", "Full-Stack Developer", "Backend Developer"],
        ),
        InstitutionalSkillDemand(
            skill="Python",
            category="Programming Languages",
            demand_percentage=84.2,
            openings_count=142,
            yoy_growth="+28%",
            recommended_for_roles=["AI/ML Engineer", "Backend Developer", "Data Engineer"],
        ),
        InstitutionalSkillDemand(
            skill="React",
            category="Frontend Development",
            demand_percentage=78.5,
            openings_count=128,
            yoy_growth="+18%",
            recommended_for_roles=["Frontend Developer", "Full-Stack Developer"],
        ),
        InstitutionalSkillDemand(
            skill="PostgreSQL / SQL",
            category="Databases",
            demand_percentage=76.0,
            openings_count=124,
            yoy_growth="+12%",
            recommended_for_roles=["Full-Stack Developer", "Backend Developer", "Data Engineer"],
        ),
        InstitutionalSkillDemand(
            skill="Docker & Containers",
            category="DevOps & Cloud",
            demand_percentage=65.4,
            openings_count=98,
            yoy_growth="+42%",
            recommended_for_roles=["DevOps / Cloud Engineer", "Backend Developer"],
        ),
        InstitutionalSkillDemand(
            skill="FastAPI / REST APIs",
            category="Backend Development",
            demand_percentage=62.0,
            openings_count=92,
            yoy_growth="+35%",
            recommended_for_roles=["Backend Developer", "AI/ML Engineer"],
        ),
        InstitutionalSkillDemand(
            skill="TypeScript",
            category="Programming Languages",
            demand_percentage=58.3,
            openings_count=86,
            yoy_growth="+30%",
            recommended_for_roles=["Frontend Developer", "Full-Stack Developer"],
        ),
        InstitutionalSkillDemand(
            skill="Large Language Models & RAG",
            category="AI & Data Science",
            demand_percentage=45.0,
            openings_count=65,
            yoy_growth="+95%",
            recommended_for_roles=["AI/ML Engineer", "Generative AI Developer"],
        ),
    ]

    if isinstance(category, str) and category.strip():
        cat_lower = category.lower().strip()
        filtered = [s for s in skills_data if cat_lower in s.category.lower() or cat_lower in s.skill.lower()]
        skills_data = filtered or skills_data

    return InstitutionalDemandResponse(
        is_mock=True,
        notice="Mock endpoint simulating campus Training & Placement Cell (T&P) hiring demand.",
        institution_name="National Institute of Technology / Campus Placement Cell",
        placement_season="2026-2027 Placement Season",
        active_recruiting_partners=48,
        total_active_openings=320,
        top_demanded_skills=skills_data,
        role_demand_breakdown={
            "Full-Stack Developer": 34.0,
            "Software Engineer (Core)": 28.0,
            "AI/ML Engineer": 18.0,
            "Data Engineer": 12.0,
            "Cloud / DevOps": 8.0,
        },
        curriculum_gap_recommendations=[
            "Introduce containerization (Docker) earlier in Semester 5 systems curriculum.",
            "Incorporate TypeScript and modern React state patterns into Web Technologies lab.",
            "Conduct hands-on RAG and LLM deployment workshops for final-year placement readiness.",
        ],
    )

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

    # Enforce 5 MiB (5 * 1024 * 1024 bytes) limit in chunks while reading
    max_bytes = 5 * 1024 * 1024
    chunk_size = 64 * 1024
    byte_chunks = []
    total_bytes = 0

    try:
        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break
            total_bytes += len(chunk)
            if total_bytes > max_bytes:
                raise HTTPException(
                    status_code=413,
                    detail="Resume must be smaller than 5 MB"
                )
            byte_chunks.append(chunk)

        file_bytes = b"".join(byte_chunks)

        # Validate PDF magic bytes (%PDF-)
        if not file_bytes.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=400,
                detail="Invalid PDF file format. The file does not have valid PDF magic bytes."
            )

        resume_text = extract_resume_text(file_bytes)

        profile = analyze_resume(resume_text)
        user, authenticated_client = auth
        save_student_profile(authenticated_client, str(user.id), profile)

        # Save to multi-resume store
        resume_record = save_student_resume(
            authenticated_client,
            student_id=str(user.id),
            label=file.filename.replace(".pdf", "").replace("_", " ").title() if file.filename else "Primary Resume",
            filename=file.filename or "resume.pdf",
            profile=profile,
            target_role=profile.career_goal or "",
            career_goal=profile.career_goal or "",
            make_active=True,
        )

        return {
            "success": True,
            "user_id": str(user.id),
            "resume_id": resume_record.get("id"),
            "profile": profile.model_dump(),
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.exception("Resume analysis failed unexpectedly: %s", e)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while analyzing the resume. Please try again later."
        )

    finally:
        await file.close()


@app.get("/api/resumes")
def get_student_resumes_endpoint(
    auth=Depends(get_current_user),
):
    """List all saved resumes for the authenticated student."""
    user, client = auth
    return list_student_resumes(client, str(user.id))


@app.post("/api/resumes/manual")
def save_manual_profile_endpoint(
    profile_data: dict,
    auth=Depends(get_current_user),
):
    """Create or update a student profile manually without requiring a PDF upload."""
    user, client = auth
    student_id = str(user.id)

    full_name = profile_data.get("full_name") or "Student"
    university = profile_data.get("university") or ""
    degree = profile_data.get("degree") or ""
    grad_year = profile_data.get("graduation_year")
    career_goal = profile_data.get("career_goal") or profile_data.get("target_role") or "Software Engineer"
    raw_skills = profile_data.get("skills") or []
    label = profile_data.get("label") or f"{career_goal} Profile"

    # Convert skill strings or dicts to Skill objects
    from .schemas.student import Skill, StudentProfile
    skill_objs = []
    for s in raw_skills:
        name = s.get("name") if isinstance(s, dict) else str(s)
        canonical = normalize_skill(name)
        cat = s.get("category", "General") if isinstance(s, dict) else "General"
        prof = s.get("proficiency", "Intermediate") if isinstance(s, dict) else "Intermediate"
        skill_objs.append(Skill(
            name=canonical,
            category=cat,
            proficiency=prof,
            confidence=0.9,
            evidence="Self-reported by candidate during profile onboarding",
        ))

    profile = StudentProfile(
        full_name=full_name,
        university=university,
        degree=degree,
        graduation_year=int(grad_year) if grad_year else None,
        career_goal=career_goal,
        skills=skill_objs,
        projects=[],
    )

    # Save to primary profile & student_skills
    save_student_profile(client, student_id, profile)

    # Save to multi-resume store
    record = save_student_resume(
        client,
        student_id=student_id,
        label=label,
        filename="manual_profile.pdf",
        profile=profile,
        target_role=career_goal,
        career_goal=career_goal,
        make_active=True,
    )

    return {
        "success": True,
        "message": "Manual profile saved successfully",
        "resume": record,
        "profile": profile.model_dump(),
    }


@app.post("/api/resumes/{resume_id}/activate")
def activate_student_resume_endpoint(
    resume_id: str,
    auth=Depends(get_current_user),
):
    """Switch active resume to a different profile version."""
    user, client = auth
    activated = set_active_resume(client, str(user.id), resume_id)
    if not activated:
        raise HTTPException(status_code=404, detail="Resume not found")

    profile_dict = activated.get("parsed_profile") or {}
    skills_list = profile_dict.get("skills") or []
    active_skills = []
    for skill in skills_list:
        if not isinstance(skill, dict) or not skill.get("name"):
            continue
        active_skills.append(
            Skill(
                name=normalize_skill(str(skill["name"])),
                category=str(skill.get("category") or "General"),
                proficiency=str(skill.get("proficiency") or "Intermediate"),
                confidence=float(skill.get("confidence", 0.9)),
                evidence=str(
                    skill.get("evidence")
                    or f"From resume: {activated.get('label')}"
                ),
            )
        )
    replace_student_skills(client, str(user.id), active_skills)

    return {
        "success": True,
        "message": f"Switched active resume to '{activated.get('label')}'",
        "active_resume": activated,
    }


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


def _assert_dev_routes_enabled():
    """Ensure dev routes are explicitly enabled via ENABLE_DEV_ROUTES=true."""
    if os.getenv("ENABLE_DEV_ROUTES", "false").lower() != "true":
        raise HTTPException(
            status_code=404,
            detail="Development route not enabled. Set ENABLE_DEV_ROUTES=true to access.",
        )


@app.post("/api/opportunities/sync-local")
async def sync_opportunity_sources_locally(request: Request):
    """Run configured source sync locally without a browser access token."""
    _assert_dev_routes_enabled()

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
    _assert_dev_routes_enabled()

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


@app.get("/api/opportunities/saved")
async def get_saved_matches_endpoint(
    limit: int = Query(default=20, ge=1, le=100),
    auth=Depends(get_current_user),
):
    """Fast-reload saved opportunity matches (candidate state) on re-login."""
    user, authenticated_client = auth
    saved = get_saved_opportunity_matches(authenticated_client, str(user.id), limit=limit)
    if saved:
        return {
            "success": True,
            "count": len(saved),
            "source": "candidate_state",
            "recommendations": saved,
        }

    # Fallback to fresh recommendation if no saved matches yet
    recommendations = recommend_opportunities(
        authenticated_client, str(user.id), limit=limit
    )
    return {
        "success": True,
        "count": len(recommendations),
        "source": "calculated_fresh",
        "recommendations": [r.model_dump() for r in recommendations],
    }


@app.get("/api/learning-roadmap")
def get_learning_roadmap_endpoint(
    auth=Depends(get_current_user),
):
    """Return deterministic target-job and shared-core learning roadmaps."""
    user, authenticated_client = auth
    student_id = str(user.id)
    preferences = get_student_preferences(authenticated_client, student_id)
    recommendations = recommend_opportunities(
        authenticated_client,
        student_id,
        location=preferences.get("preferred_location") or None,
        job_type=preferences.get("preferred_job_type") or None,
        remote=bool(preferences.get("remote_only", False)),
        minimum_score=float(preferences.get("minimum_score") or 0),
        limit=5,
    )
    skill_rows = (
        authenticated_client.table("student_skills")
        .select("skills(name)")
        .eq("student_id", student_id)
        .execute()
    )
    student_skills = []
    for row in skill_rows.data or []:
        nested = row.get("skills")
        if isinstance(nested, dict) and nested.get("name"):
            student_skills.append(str(nested["name"]))
        elif isinstance(nested, list) and nested and nested[0].get("name"):
            student_skills.append(str(nested[0]["name"]))

    roadmaps = build_learning_roadmaps(
        recommendations,
        student_skills,
        get_framework_engine().documents,
    )
    progress = get_student_learning_progress(authenticated_client, student_id)
    return {"success": True, "progress": progress, **roadmaps}


@app.put("/api/learning-progress")
def update_learning_progress_endpoint(
    request: LearningProgressUpdate,
    auth=Depends(get_current_user),
):
    """Save evidence-backed progress for the authenticated student's skill."""
    user, authenticated_client = auth
    progress = save_student_learning_progress(
        authenticated_client,
        str(user.id),
        request,
    )
    return {"success": True, "progress": progress}


@app.post("/api/chat", response_model=ChatMessageResponse)
async def conversational_refinement(
    request: ChatMessageRequest,
    auth=Depends(get_current_user),
):
    """Conversational refinement: Groq extracts PreferenceUpdate, updates preferences, re-runs matching."""
    user, authenticated_client = auth
    student_id = str(user.id)

    curr_prefs = get_student_preferences(authenticated_client, student_id)
    pref_update = parse_conversational_preference(request.message, curr_prefs)

    # Merge updates
    merged = dict(curr_prefs)
    if pref_update.preferred_location is not None:
        merged["preferred_location"] = pref_update.preferred_location
    if pref_update.remote_only is not None:
        merged["remote_only"] = pref_update.remote_only
    if pref_update.preferred_job_type is not None:
        merged["preferred_job_type"] = pref_update.preferred_job_type
    if pref_update.preferred_skills:
        merged["preferred_skills"] = pref_update.preferred_skills
    if pref_update.target_role is not None:
        merged["target_role"] = pref_update.target_role
    if pref_update.minimum_score is not None:
        merged["minimum_score"] = pref_update.minimum_score

    # Save to candidate preferences state
    save_student_preferences(authenticated_client, student_id, merged)

    # Re-run matching step with refined preferences
    recommendations = recommend_opportunities(
        authenticated_client,
        student_id,
        location=merged.get("preferred_location") or None,
        job_type=merged.get("preferred_job_type") or None,
        remote=bool(merged.get("remote_only", False)),
        minimum_score=float(merged.get("minimum_score") or 0),
        limit=20,
    )

    return ChatMessageResponse(
        success=True,
        user_message=request.message,
        reply=pref_update.assistant_message,
        filters_applied=pref_update.filters_applied,
        preferences=merged,
        count=len(recommendations),
        recommendations=recommendations,
    )


@app.post("/api/chat-local", response_model=ChatMessageResponse)
async def local_conversational_refinement(
    request: ChatMessageRequest,
):
    """Local dev test chat endpoint using MATCHING_TEST_STUDENT_ID."""
    _assert_dev_routes_enabled()

    student_id = os.getenv("MATCHING_TEST_STUDENT_ID", "dev-student-001").strip()
    client = get_service_client()

    curr_prefs = get_student_preferences(client, student_id)
    pref_update = parse_conversational_preference(request.message, curr_prefs)

    merged = dict(curr_prefs)
    if pref_update.preferred_location is not None:
        merged["preferred_location"] = pref_update.preferred_location
    if pref_update.remote_only is not None:
        merged["remote_only"] = pref_update.remote_only
    if pref_update.preferred_job_type is not None:
        merged["preferred_job_type"] = pref_update.preferred_job_type
    if pref_update.preferred_skills:
        merged["preferred_skills"] = pref_update.preferred_skills
    if pref_update.target_role is not None:
        merged["target_role"] = pref_update.target_role
    if pref_update.minimum_score is not None:
        merged["minimum_score"] = pref_update.minimum_score

    save_student_preferences(client, student_id, merged)

    recommendations = recommend_opportunities(
        client,
        student_id,
        location=merged.get("preferred_location") or None,
        job_type=merged.get("preferred_job_type") or None,
        remote=bool(merged.get("remote_only", False)),
        minimum_score=float(merged.get("minimum_score") or 0),
        limit=20,
    )

    return ChatMessageResponse(
        success=True,
        user_message=request.message,
        reply=pref_update.assistant_message,
        filters_applied=pref_update.filters_applied,
        preferences=merged,
        count=len(recommendations),
        recommendations=recommendations,
    )


@app.post("/api/agent/run", response_model=AgentRunResponse)
async def run_planner_executor_agent(
    request: AgentRunRequest,
    auth=Depends(get_current_user),
):
    """Planner-Executor endpoint: Groq plans steps (profile, retrieve, match, roadmap), Executor runs them."""
    user, authenticated_client = auth
    student_id = str(user.id)

    # 1. Initialize shared agent state
    state = AgentState(
        student_id=student_id,
        resume_text=request.resume_text,
        preferences=request.preferences,
    )

    # 2. Planner decomposes the goal into an ordered step plan
    plan = generate_agent_plan(
        goal=request.goal,
        context={
            "has_profile": False,
            "has_resume_text": bool(request.resume_text),
        },
    )

    # 3. Executor runs each step sequentially with shared state
    final_state = execute_plan(plan, state, client=authenticated_client)
    roadmap_step_count = sum(
        len(section.get("steps", [])) for section in final_state.roadmap
    )

    summary = (
        f"Executed {len(final_state.execution_trace)} steps successfully. "
        f"Found {len(final_state.matches)} matching opportunities and "
        f"generated {roadmap_step_count} evidence-based roadmap steps."
    )

    return AgentRunResponse(
        success=True,
        goal=request.goal,
        plan=plan,
        execution_trace=final_state.execution_trace,
        profile_summary=final_state.profile,
        matches_count=len(final_state.matches),
        top_matches=final_state.matches[:5],
        roadmap=final_state.roadmap,
        summary=summary,
    )


@app.post("/api/agent/run-local", response_model=AgentRunResponse)
async def run_planner_executor_agent_local(
    request: AgentRunRequest,
):
    """Local dev test endpoint for planner-executor agent."""
    _assert_dev_routes_enabled()

    student_id = os.getenv("MATCHING_TEST_STUDENT_ID", "dev-student-001").strip()
    client = get_service_client()

    state = AgentState(
        student_id=student_id,
        resume_text=request.resume_text,
        preferences=request.preferences,
    )

    plan = generate_agent_plan(
        goal=request.goal,
        context={
            "has_profile": False,
            "has_resume_text": bool(request.resume_text),
        },
    )

    final_state = execute_plan(plan, state, client=client)
    roadmap_step_count = sum(
        len(section.get("steps", [])) for section in final_state.roadmap
    )

    summary = (
        f"Executed {len(final_state.execution_trace)} steps successfully. "
        f"Found {len(final_state.matches)} matching opportunities and "
        f"generated {roadmap_step_count} evidence-based roadmap steps."
    )

    return AgentRunResponse(
        success=True,
        goal=request.goal,
        plan=plan,
        execution_trace=final_state.execution_trace,
        profile_summary=final_state.profile,
        matches_count=len(final_state.matches),
        top_matches=final_state.matches[:5],
        roadmap=final_state.roadmap,
        summary=summary,
    )

