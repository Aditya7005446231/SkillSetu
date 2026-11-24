"""Verification suite for candidate state persistence, LLM retry validation, and conversational refinement."""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.schemas.opportunity import RecommendedOpportunity
from app.schemas.preference import PreferenceUpdate, ChatMessageRequest
from app.services.candidate_state_persistence import (
    save_student_preferences,
    get_student_preferences,
    save_opportunity_matches,
    get_saved_opportunity_matches,
)
from app.services.llm_validator import call_llm_with_validation
from app.agents.chat_agent import parse_conversational_preference


def run_tests():
    print("=" * 70)
    print("   CONVERSATIONAL REFINEMENT & CANDIDATE STATE TEST SUITE")
    print("=" * 70)

    student_id = "test-student-candidate-001"

    # 1. Candidate State: Student Preferences Persistence Test
    print("\n[TEST 1] Testing Student Preferences Persistence...")
    initial_prefs = {
        "preferred_location": "Bangalore",
        "remote_only": True,
        "preferred_job_type": "internship",
        "preferred_skills": ["React", "FastAPI"],
        "minimum_score": 75.0,
    }
    saved_prefs = save_student_preferences(None, student_id, initial_prefs)
    assert saved_prefs["student_id"] == student_id
    assert saved_prefs["remote_only"] is True
    assert saved_prefs["preferred_location"] == "Bangalore"

    retrieved = get_student_preferences(None, student_id)
    assert retrieved["preferred_job_type"] == "internship"
    assert retrieved["minimum_score"] == 75.0
    print(" PASS: Student preferences saved and retrieved successfully.")

    # 2. Candidate State: Opportunity Matches Persistence Test
    print("\n[TEST 2] Testing Opportunity Matches (Candidate State) Persistence...")
    dummy_matches = [
        RecommendedOpportunity(
            job_id="job-uuid-101",
            title="Frontend Developer Intern",
            company="TechCorp",
            location="Bangalore",
            job_type="internship",
            apply_url="https://example.com/apply/101",
            match_score=88.5,
            matched_skills=["React", "JavaScript", "TypeScript"],
            missing_skills=["Next.js"],
            related_gap_skills={"Next.js": ["React", "Server-Side Rendering"]},
            reason="Matched React, JavaScript, TypeScript. Missing Next.js.",
            formula_version="coverage-location-type-v2-rag",
        ),
        RecommendedOpportunity(
            job_id="job-uuid-102",
            title="Python AI Intern",
            company="AILabs",
            location="Remote",
            job_type="internship",
            apply_url="https://example.com/apply/102",
            match_score=82.0,
            matched_skills=["Python", "FastAPI"],
            missing_skills=["PyTorch"],
            related_gap_skills={"PyTorch": ["Deep Learning", "NumPy"]},
            reason="Matched Python, FastAPI. Missing PyTorch.",
            formula_version="coverage-location-type-v2-rag",
        ),
    ]

    saved_count = save_opportunity_matches(None, student_id, dummy_matches)
    assert saved_count == 2, f"Expected 2 matches saved, got {saved_count}"

    loaded_matches = get_saved_opportunity_matches(None, student_id, limit=5)
    assert len(loaded_matches) == 2, f"Expected 2 matches loaded, got {len(loaded_matches)}"
    assert loaded_matches[0]["job_id"] == "job-uuid-101"
    assert loaded_matches[0]["match_score"] == 88.5
    assert loaded_matches[0]["matched_skills"] == ["React", "JavaScript", "TypeScript"]
    print(f" PASS: {saved_count} candidate state matches persisted and fast-loaded on re-login.")

    # 3. LLM Validation & Retry Engine Test
    print("\n[TEST 3] Testing LLM Validation & Retry Engine...")
    test_prompt = """
    Extract structured preferences from: "I want remote full-time positions with Python and Docker, score above 80%"
    Return JSON with fields:
    - preferred_location: null
    - remote_only: true
    - preferred_job_type: "full-time"
    - preferred_skills: ["Python", "Docker"]
    - minimum_score: 80.0
    - assistant_message: "Here are remote full-time roles."
    - filters_applied: ["Remote Only", "Full-time"]
    """
    pref_update = call_llm_with_validation(
        schema=PreferenceUpdate,
        prompt=test_prompt,
        system_prompt="Return only valid JSON strictly matching the requested PreferenceUpdate schema.",
        temperature=0.0,
        max_retries=1,
    )
    assert isinstance(pref_update, PreferenceUpdate), "Result must be a validated PreferenceUpdate"
    assert pref_update.remote_only is True, f"Expected remote_only to be True, got {pref_update.remote_only}"
    assert pref_update.preferred_job_type == "full-time", f"Expected full-time, got {pref_update.preferred_job_type}"
    print(f" PASS: Validated Pydantic output: remote={pref_update.remote_only}, job_type={pref_update.preferred_job_type}")
    print(f"       Assistant response: {pref_update.assistant_message[:70]}...")

    # 4. Conversational Refinement Parsing Test
    print("\n[TEST 4] Testing Conversational Refinement Parser...")
    user_query = "Only show me remote internships in Bangalore with React"
    refinement = parse_conversational_preference(user_query, current_preferences=retrieved)

    assert refinement.remote_only is True, "Expected remote_only to be True"
    assert refinement.preferred_job_type == "internship", f"Expected internship, got {refinement.preferred_job_type}"
    assert "Bangalore" in (refinement.preferred_location or ""), f"Expected Bangalore in location, got {refinement.preferred_location}"
    assert "React" in refinement.preferred_skills, f"Expected React in skills, got {refinement.preferred_skills}"
    print(f" PASS: Conversational parser extracted:")
    print(f"       - Remote only: {refinement.remote_only}")
    print(f"       - Location: {refinement.preferred_location}")
    print(f"       - Job Type: {refinement.preferred_job_type}")
    print(f"       - Preferred Skills: {refinement.preferred_skills}")
    print(f"       - Badges: {refinement.filters_applied}")
    print(f"       - Assistant Reply: {refinement.assistant_message}")

    print("\n" + "=" * 70)
    print("   ALL CONVERSATIONAL REFINEMENT & STATE TESTS PASSED!")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
