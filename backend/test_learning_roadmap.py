"""Tests for deterministic, recommendation-grounded learning roadmaps."""

import sys
from pathlib import Path
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.agents.executor import AgentState, step_roadmap
from app.schemas.agent_plan import PlanStep
from app.services.learning_roadmap import build_learning_roadmaps


FRAMEWORK = [
    {"title": "Python", "prerequisites": []},
    {"title": "Linux", "prerequisites": []},
    {"title": "Docker", "prerequisites": ["Linux"]},
    {"title": "FastAPI", "prerequisites": ["Python"]},
    {"title": "SQL", "prerequisites": []},
    {"title": "React", "prerequisites": []},
]


class LearningRoadmapTests(unittest.TestCase):
    def setUp(self):
        canonical = {
            skill.lower(): skill
            for skill in ("Python", "Linux", "Docker", "FastAPI", "SQL", "React")
        }
        self.normalize_patch = patch(
            "app.services.learning_roadmap.normalize_skill",
            side_effect=lambda skill: canonical.get(
                skill.strip().lower(), skill.strip()
            ),
        )
        self.normalize_patch.start()
        self.addCleanup(self.normalize_patch.stop)

    def test_target_roadmap_orders_missing_prerequisites_before_job_skills(self):
        result = build_learning_roadmaps(
            [
                {
                    "job_id": "backend-role",
                    "title": "Backend Developer",
                    "company": "Example",
                    "match_score": 80,
                    "missing_skills": ["FastAPI", "Docker"],
                }
            ],
            ["Python"],
            FRAMEWORK,
        )

        target = result["target_roadmaps"][0]
        self.assertEqual(
            [step["skill"] for step in target["steps"]],
            ["Linux", "Docker", "FastAPI"],
        )
        self.assertEqual(target["steps"][0]["kind"], "prerequisite")
        self.assertEqual(target["steps"][1]["kind"], "job_requirement")
        self.assertIn("Backend Developer", target["steps"][1]["reason"])
        self.assertIn("Backend Developer", target["steps"][1]["learning_task"])
        self.assertTrue(target["steps"][1]["acceptance_criteria"])

    def test_shared_core_uses_repeated_gaps_and_excludes_one_off_gaps(self):
        result = build_learning_roadmaps(
            [
                {
                    "job_id": "job-1",
                    "title": "Role One",
                    "match_score": 90,
                    "missing_skills": ["SQL", "Docker", "React"],
                },
                {
                    "job_id": "job-2",
                    "title": "Role Two",
                    "match_score": 80,
                    "missing_skills": ["SQL", "Docker"],
                },
                {
                    "job_id": "job-3",
                    "title": "Role Three",
                    "match_score": 70,
                    "missing_skills": ["SQL"],
                },
            ],
            [],
            FRAMEWORK,
        )

        core = result["shared_core"]
        self.assertEqual(
            [(skill["name"], skill["occurrences"]) for skill in core["skills"]],
            [("SQL", 3), ("Docker", 2)],
        )
        self.assertNotIn("React", [skill["name"] for skill in core["skills"]])

    def test_known_prerequisite_is_not_repeated_as_a_learning_gap(self):
        result = build_learning_roadmaps(
            [
                {
                    "job_id": "docker-role",
                    "title": "Platform Engineer",
                    "match_score": 75,
                    "missing_skills": ["Docker"],
                }
            ],
            ["Linux"],
            FRAMEWORK,
        )

        steps = result["target_roadmaps"][0]["steps"]
        self.assertEqual([step["skill"] for step in steps], ["Docker"])
        self.assertEqual(steps[0]["prerequisites"], [])

    def test_empty_recommendations_do_not_create_generic_gaps(self):
        result = build_learning_roadmaps([], ["Python"], FRAMEWORK)

        self.assertEqual(result["target_roadmaps"], [])
        self.assertEqual(result["shared_core"]["skills"], [])
        self.assertEqual(result["shared_core"]["steps"], [])
        self.assertIn("No skill gap appears", result["shared_core"]["message"])

    def test_roadmap_order_is_repeatable(self):
        matches = [
            {
                "job_id": "job-1",
                "title": "Backend Developer",
                "match_score": 80,
                "missing_skills": ["FastAPI", "Docker"],
            }
        ]

        first = build_learning_roadmaps(matches, ["Python"], FRAMEWORK)
        second = build_learning_roadmaps(matches, ["Python"], FRAMEWORK)

        self.assertEqual(first, second)

    def test_agent_executor_returns_target_and_shared_roadmaps(self):
        state = AgentState("student-1")
        state.student_skills = ["Python"]
        state.matches = [
            {
                "job_id": "job-1",
                "title": "Backend Developer",
                "company": "One",
                "match_score": 80,
                "missing_skills": ["Docker"],
            },
            {
                "job_id": "job-2",
                "title": "Platform Developer",
                "company": "Two",
                "match_score": 75,
                "missing_skills": ["Docker"],
            },
        ]
        step = PlanStep(
            step="roadmap",
            title="Build roadmap",
            description="Use recommendation-backed gaps.",
        )

        with patch(
            "app.agents.executor.get_framework_engine",
            return_value=type("Engine", (), {"documents": FRAMEWORK})(),
        ):
            step_roadmap(state, step, None)

        self.assertEqual(
            [section["type"] for section in state.roadmap],
            ["target_job", "target_job", "shared_core"],
        )
        self.assertEqual(state.roadmap[-1]["skills"][0]["occurrences"], 2)


if __name__ == "__main__":
    unittest.main()
