"""Executor Agent: Runs an ordered step plan using a shared state object and step dispatch dict."""

import time
import logging
from typing import Any, Callable

from supabase import Client

from ..schemas.agent_plan import AgentPlan, PlanStep
from ..services.opportunity_matching import recommend_opportunities
from ..services.candidate_state_persistence import get_student_preferences
from ..services.learning_roadmap import build_learning_roadmaps
from ..services.skill_framework_rag import get_framework_engine

logger = logging.getLogger(__name__)


class AgentState:
    """Shared state object carrying context across step executions."""

    def __init__(self, student_id: str, resume_text: str | None = None, preferences: dict | None = None):
        self.student_id = student_id
        self.resume_text = resume_text
        self.preferences = preferences or {}
        self.profile: dict[str, Any] | None = None
        self.student_skills: list[str] = []
        self.retrieved_jobs_count: int = 0
        self.matches: list[dict[str, Any]] = []
        self.roadmap: list[dict[str, Any]] = []
        self.execution_trace: list[dict[str, Any]] = []

    def to_dict(self) -> dict[str, Any]:
        return {
            "student_id": self.student_id,
            "has_profile": self.profile is not None,
            "profile_summary": self.profile,
            "student_skills_count": len(self.student_skills),
            "retrieved_jobs_count": self.retrieved_jobs_count,
            "matches_count": len(self.matches),
            "top_matches": self.matches[:5],
            "roadmap": self.roadmap,
            "execution_trace": self.execution_trace,
        }


def step_profile(state: AgentState, step: PlanStep, client: Client | None) -> None:
    """Step 1: Profile candidate skills from new resume text or load from database."""
    if state.resume_text and len(state.resume_text.strip()) > 50:
        from .skill_profiling import analyze_resume
        from ..services.profile_persistence import save_student_profile

        profile = analyze_resume(state.resume_text)
        state.profile = profile.model_dump()
        state.student_skills = [s.name for s in profile.skills]

        if client:
            try:
                save_student_profile(client, state.student_id, profile)
            except Exception as e:
                logger.warning("Could not persist parsed profile: %s", e)
    elif client:
        # Load existing profile and skills from Supabase
        try:
            prof_res = (
                client.table("profiles")
                .select("*")
                .eq("id", state.student_id)
                .maybe_single()
                .execute()
            )
            skills_res = (
                client.table("student_skills")
                .select("skills(name)")
                .eq("student_id", state.student_id)
                .execute()
            )
            state.profile = prof_res.data if prof_res else {}
            extracted = []
            for row in (skills_res.data or []):
                s = row.get("skills")
                if isinstance(s, dict) and s.get("name"):
                    extracted.append(s["name"])
            state.student_skills = extracted
        except Exception as e:
            logger.warning("Failed loading profile from DB: %s", e)

def step_retrieve(state: AgentState, step: PlanStep, client: Client | None) -> None:
    """Step 2: Retrieve active job pool from database."""
    if client:
        try:
            res = (
                client.table("jobs")
                .select("id")
                .eq("is_active", True)
                .limit(200)
                .execute()
            )
            state.retrieved_jobs_count = len(res.data or [])
        except Exception as e:
            logger.warning("Failed querying active jobs count: %s", e)
    else:
        state.retrieved_jobs_count = 0


def step_match(state: AgentState, step: PlanStep, client: Client | None) -> None:
    """Step 3: Run matching algorithm and save candidate state."""
    prefs = state.preferences
    if not prefs and client:
        prefs = get_student_preferences(client, state.student_id)

    loc = prefs.get("preferred_location") or None
    jtype = prefs.get("preferred_job_type") or None
    remote = bool(prefs.get("remote_only", False))
    min_score = float(prefs.get("minimum_score") or 0.0)

    if client:
        try:
            recommendations = recommend_opportunities(
                client,
                state.student_id,
                location=loc,
                job_type=jtype,
                remote=remote,
                minimum_score=min_score,
                limit=15,
            )
            state.matches = [r.model_dump() for r in recommendations]
        except Exception as e:
            logger.warning("Matching step encountered error: %s", e)


def step_roadmap(state: AgentState, step: PlanStep, client: Client | None) -> None:
    """Build deterministic target-job and shared-core roadmaps from verified matches."""
    engine = get_framework_engine()
    result = build_learning_roadmaps(
        state.matches,
        state.student_skills,
        engine.documents,
    )
    state.roadmap = [
        {"type": "target_job", **roadmap}
        for roadmap in result["target_roadmaps"]
    ]
    if result["shared_core"]["skills"]:
        state.roadmap.append(
            {"type": "shared_core", **result["shared_core"]}
        )


STEP_DISPATCH: dict[str, Callable[[AgentState, PlanStep, Client | None], None]] = {
    "profile": step_profile,
    "retrieve": step_retrieve,
    "match": step_match,
    "roadmap": step_roadmap,
}


def execute_plan(
    plan: AgentPlan,
    state: AgentState,
    client: Client | None = None,
) -> AgentState:
    """Execute each step in the generated plan sequentially using shared state."""
    logger.info("Executing plan for student %s: %d steps", state.student_id, len(plan.steps))

    for step in plan.steps:
        step_func = STEP_DISPATCH.get(step.step)
        if not step_func:
            logger.warning("Unrecognized step '%s' skipped.", step.step)
            continue

        t0 = time.perf_counter()
        status = "success"
        err_msg = None

        try:
            step_func(state, step, client)
        except Exception as e:
            status = "failed"
            err_msg = str(e)
            logger.exception("Step '%s' failed: %s", step.step, e)

        elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)
        state.execution_trace.append(
            {
                "step": step.step,
                "title": step.title,
                "status": status,
                "latency_ms": elapsed_ms,
                "error": err_msg,
            }
        )

    return state
