"""Verification suite for Planner-Executor Agent architecture (/api/agent/run)."""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.schemas.agent_plan import AgentPlan, AgentRunRequest
from app.agents.planner import generate_agent_plan
from app.agents.executor import AgentState, execute_plan


def run_tests():
    print("=" * 70)
    print("   PLANNER-EXECUTOR AGENT ORCHESTRATION TEST SUITE")
    print("=" * 70)

    # 1. Test Planner Decomposition
    print("\n[TEST 1] Testing Planner Decomposition into Step Plan...")
    user_goal = "Analyze my resume, match me to top remote frontend internships, and plan my learning roadmap"
    
    plan = generate_agent_plan(user_goal, context={"has_profile": False, "has_resume_text": False})
    
    assert isinstance(plan, AgentPlan), "Plan must be an instance of AgentPlan"
    assert len(plan.steps) >= 2, f"Expected at least 2 steps, got {len(plan.steps)}"
    step_names = [s.step for s in plan.steps]
    print(f" PASS: Planner formulated goal into {len(plan.steps)} steps:")
    for idx, s in enumerate(plan.steps, 1):
        print(f"       {idx}. [{s.step}] {s.title} - {s.description}")
    
    allowed = {"profile", "retrieve", "match", "roadmap"}
    for name in step_names:
        assert name in allowed, f"Step '{name}' is not in allowed capability set {allowed}"
    print(f" PASS: All steps strictly belong to allowed capability set.")

    # 2. Test Shared Agent State Initialization
    print("\n[TEST 2] Testing Shared Agent State Initialization...")
    student_id = "test-agent-student-999"
    state = AgentState(
        student_id=student_id,
        resume_text=None,
        preferences={"remote_only": True, "preferred_location": "Bangalore"},
    )
    assert state.student_id == student_id
    assert state.preferences["remote_only"] is True
    print(" PASS: Shared state initialized with student context and preferences.")

    # 3. Test Sequential Step Execution (Executor)
    print("\n[TEST 3] Testing Step Execution with Step Dispatch...")
    final_state = execute_plan(plan, state, client=None)
    
    assert len(final_state.execution_trace) == len(plan.steps), "Trace count must match plan step count"
    print(f" PASS: Executed {len(final_state.execution_trace)} steps:")
    for trace in final_state.execution_trace:
        assert trace["status"] == "success", f"Step '{trace['step']}' failed: {trace.get('error')}"
        print(f"       [{trace['step']}] {trace['title']}: {trace['status']} in {trace['latency_ms']} ms")

    # 4. Verify Final State Deliverables
    print("\n[TEST 4] Verifying Final State Deliverables...")
    state_dict = final_state.to_dict()
    assert state_dict["has_profile"] is True, "Profile must be populated"
    assert state_dict["matches_count"] > 0, "Matches must be populated"
    assert len(state_dict["roadmap"]) == 4, f"Roadmap must have 4 milestones, got {len(state_dict['roadmap'])}"
    
    print(f" PASS: Deliverables generated:")
    print(f"       - Profile Skills: {final_state.student_skills}")
    print(f"       - Matches Found: {len(final_state.matches)}")
    print(f"       - Roadmap Milestones: {len(final_state.roadmap)}")
    for milestone in final_state.roadmap:
        print(f"         Milestone {milestone['milestone']}: {milestone['title']} ({milestone['status']})")

    print("\n" + "=" * 70)
    print("   ALL PLANNER-EXECUTOR TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
