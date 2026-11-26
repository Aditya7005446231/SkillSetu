"""API checks for authenticated recommendation isolation."""

import sys
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastapi.testclient import TestClient

from app.main import app, get_current_user


class RecommendationApiTests(unittest.TestCase):
    def setUp(self):
        self.previous_overrides = app.dependency_overrides.copy()

    def tearDown(self):
        app.dependency_overrides.clear()
        app.dependency_overrides.update(self.previous_overrides)

    def test_recommendations_require_authentication(self):
        app.dependency_overrides.pop(get_current_user, None)

        with TestClient(app) as client:
            response = client.get("/api/opportunities/recommended")

        self.assertEqual(response.status_code, 401)

    def test_query_cannot_override_authenticated_student_id(self):
        authenticated_user = SimpleNamespace(id="student-authenticated")
        authenticated_client = object()
        app.dependency_overrides[get_current_user] = (
            lambda: (authenticated_user, authenticated_client)
        )

        with patch("app.main.recommend_opportunities", return_value=[]) as matcher:
            with TestClient(app) as client:
                response = client.get(
                    "/api/opportunities/recommended",
                    params={"student_id": "student-attacker"},
                )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["recommendations"], [])
        matcher.assert_called_once()
        self.assertEqual(matcher.call_args.args[0], authenticated_client)
        self.assertEqual(matcher.call_args.args[1], "student-authenticated")


if __name__ == "__main__":
    unittest.main()
