"""Authentication and student isolation checks for learning roadmaps."""

import sys
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi.testclient import TestClient

from app.main import app, get_current_user


class FakeStudentSkillsQuery:
    def __init__(self, table_name):
        self.table_name = table_name

    def select(self, *_args):
        return self

    def eq(self, *_args):
        return self

    def execute(self):
        data = (
            [{"skills": {"name": "Python"}}]
            if self.table_name == "student_skills"
            else []
        )
        return SimpleNamespace(data=data)


class FakeAuthenticatedClient:
    def table(self, name):
        return FakeStudentSkillsQuery(name)


class LearningRoadmapApiTests(unittest.TestCase):
    def setUp(self):
        self.previous_overrides = app.dependency_overrides.copy()

    def tearDown(self):
        app.dependency_overrides.clear()
        app.dependency_overrides.update(self.previous_overrides)

    def test_roadmap_requires_authentication(self):
        app.dependency_overrides.pop(get_current_user, None)

        with TestClient(app) as client:
            response = client.get("/api/learning-roadmap")

        self.assertEqual(response.status_code, 401)

    def test_roadmap_uses_authenticated_student_not_query_student_id(self):
        authenticated_user = SimpleNamespace(id="student-authenticated")
        authenticated_client = FakeAuthenticatedClient()
        app.dependency_overrides[get_current_user] = (
            lambda: (authenticated_user, authenticated_client)
        )

        with (
            patch("app.main.get_student_preferences", return_value={}),
            patch("app.main.recommend_opportunities", return_value=[]) as matcher,
            patch(
                "app.main.get_framework_engine",
                return_value=SimpleNamespace(documents=[]),
            ),
            patch(
                "app.main.build_learning_roadmaps",
                return_value={
                    "available_jobs": [],
                    "target_roadmaps": [],
                    "shared_core": {"skills": [], "steps": []},
                },
            ) as builder,
        ):
            with TestClient(app) as client:
                response = client.get(
                    "/api/learning-roadmap",
                    params={"student_id": "student-attacker"},
                )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertEqual(response.json()["progress"], [])
        self.assertEqual(matcher.call_args.args[1], "student-authenticated")
        builder.assert_called_once_with([], ["Python"], [])

    def test_progress_update_requires_authentication(self):
        app.dependency_overrides.pop(get_current_user, None)

        with TestClient(app) as client:
            response = client.put(
                "/api/learning-progress",
                json={
                    "skill_name": "Python",
                    "status": "in_progress",
                },
            )

        self.assertEqual(response.status_code, 401)

    def test_progress_update_uses_authenticated_student_id(self):
        authenticated_user = SimpleNamespace(id="student-authenticated")
        authenticated_client = FakeAuthenticatedClient()
        app.dependency_overrides[get_current_user] = (
            lambda: (authenticated_user, authenticated_client)
        )
        stored_progress = {
            "skill_name": "Python",
            "status": "in_progress",
        }

        with patch(
            "app.main.save_student_learning_progress",
            return_value=stored_progress,
        ) as save_progress:
            with TestClient(app) as client:
                response = client.put(
                    "/api/learning-progress",
                    json={
                        "student_id": "student-attacker",
                        "skill_name": "Python",
                        "status": "in_progress",
                    },
                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["progress"], stored_progress)
        self.assertEqual(save_progress.call_args.args[1], "student-authenticated")

    def test_completion_without_evidence_is_rejected(self):
        app.dependency_overrides[get_current_user] = (
            lambda: (
                SimpleNamespace(id="student-authenticated"),
                FakeAuthenticatedClient(),
            )
        )

        with TestClient(app) as client:
            response = client.put(
                "/api/learning-progress",
                json={
                    "skill_name": "Python",
                    "status": "completed",
                },
            )

        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
