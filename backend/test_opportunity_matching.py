"""Focused tests for resume-driven opportunity recommendations."""

import sys
from pathlib import Path
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.schemas.opportunity import RecommendedOpportunity
from app.schemas.student import Skill, StudentProfile
from app.services import opportunity_matching
from app.services.candidate_state_persistence import save_opportunity_matches
from app.services.profile_persistence import save_student_profile


class FakeResponse:
    def __init__(self, data):
        self.data = data


class FakeQuery:
    def __init__(self, client, table):
        self.client = client
        self.name = table
        self.operation = "select"
        self.filters = []
        self.payload = None

    def select(self, *_args):
        self.operation = "select"
        return self

    def eq(self, key, value):
        self.filters.append((key, value))
        return self

    def in_(self, key, values):
        self.filters.append((key, set(values)))
        return self

    def limit(self, _value):
        return self

    def upsert(self, payload, on_conflict=None):
        self.operation = "upsert"
        self.payload = payload
        self.on_conflict = on_conflict
        return self

    def delete(self):
        self.operation = "delete"
        return self

    def insert(self, payload):
        self.operation = "insert"
        self.payload = payload
        return self

    def execute(self):
        rows = self.client.tables.setdefault(self.name, [])
        matching = [
            row for row in rows
            if all(
                row.get(key) in value if isinstance(value, set)
                else row.get(key) == value
                for key, value in self.filters
            )
        ]

        if self.operation == "delete":
            self.client.tables[self.name] = [
                row for row in rows if row not in matching
            ]
            return FakeResponse(matching)
        if self.operation == "upsert":
            keys = (self.on_conflict or "").split(",")
            existing = next(
                (
                    row for row in rows
                    if keys and all(
                        row.get(key.strip()) == self.payload.get(key.strip())
                        for key in keys
                    )
                ),
                None,
            )
            if existing:
                existing.update(self.payload)
                return FakeResponse([existing])
            row = dict(self.payload)
            if self.name == "skills":
                row.setdefault("id", f"skill-{len(rows) + 1}")
            rows.append(row)
            return FakeResponse([row])
        if self.operation == "insert":
            rows.append(self.payload)
            return FakeResponse([self.payload])
        return FakeResponse(matching)


class FakeClient:
    def __init__(self, tables):
        self.tables = tables

    def table(self, name):
        return FakeQuery(self, name)


class OpportunityMatchingTests(unittest.TestCase):
    def setUp(self):
        self.client = FakeClient({
            "student_skills": [],
            "jobs": [],
            "job_skills": [],
            "opportunity_matches": [
                {"student_id": "student-1", "job_id": "old-job"}
            ],
        })
        self.normalize_patch = patch.object(
            opportunity_matching,
            "normalize_skill",
            side_effect=lambda value: value.strip().lower(),
        )
        self.related_patch = patch.object(
            opportunity_matching, "get_related_skills", return_value=[]
        )
        self.save_patch = patch.object(
            opportunity_matching, "save_opportunity_matches"
        )
        self.normalize_patch.start()
        self.related_patch.start()
        self.save_mock = self.save_patch.start()
        self.addCleanup(self.normalize_patch.stop)
        self.addCleanup(self.related_patch.stop)
        self.addCleanup(self.save_patch.stop)

    def _add_job(
        self,
        job_id,
        requirements,
        apply_url="https://jobs.example/apply",
        location="Remote",
        job_type="internship",
        is_active=True,
    ):
        self.client.tables["jobs"].append({
            "id": job_id,
            "title": f"Role {job_id}",
            "company": "Example",
            "location": location,
            "job_type": job_type,
            "apply_url": apply_url,
            "is_active": is_active,
            "last_seen_at": "2026-01-01T00:00:00+00:00",
        })
        for skill in requirements:
            self.client.tables["job_skills"].append({
                "job_id": job_id,
                "importance": 1,
                "skills": {"name": skill},
            })

    def _add_student_skills(self, *skills):
        self.client.tables["student_skills"] = [
            {"student_id": "student-1", "skills": {"name": skill}}
            for skill in skills
        ]

    def test_no_student_skills_returns_no_recommendations_and_clears_old_matches(self):
        self._add_job("job-1", ["Python"])
        matches = opportunity_matching.recommend_opportunities(
            self.client, "student-1"
        )

        self.assertEqual(matches, [])
        self.save_mock.assert_called_once_with(
            self.client, "student-1", []
        )

    def test_requires_matching_skill_requirements_and_valid_apply_url(self):
        self._add_student_skills("Python")
        self._add_job("no-requirements", [])
        self._add_job("invalid-url", ["Python"], "javascript:alert(1)")
        self._add_job("no-overlap", ["Rust"])
        self._add_job("valid", ["Python", "SQL"])

        matches = opportunity_matching.recommend_opportunities(
            self.client, "student-1"
        )

        self.assertEqual([match.job_id for match in matches], ["valid"])
        self.assertEqual(matches[0].matched_skills, ["python"])
        self.assertEqual(matches[0].missing_skills, ["sql"])
        self.assertEqual(matches[0].match_score, 50.0)
        self.assertEqual(matches[0].apply_url, "https://jobs.example/apply")

    def test_active_location_and_job_type_filters_are_applied(self):
        self._add_student_skills("Python")
        self._add_job("remote-internship", ["Python"])
        self._add_job(
            "city-full-time",
            ["Python"],
            location="Bengaluru",
            job_type="full-time",
        )
        self._add_job(
            "inactive-remote",
            ["Python"],
            is_active=False,
        )

        matches = opportunity_matching.recommend_opportunities(
            self.client,
            "student-1",
            location="Remote",
            job_type="internship",
            remote=True,
        )

        self.assertEqual([match.job_id for match in matches], ["remote-internship"])

    def test_ranking_and_scores_are_reproducible(self):
        self._add_student_skills("Python", "SQL")
        self._add_job(
            "partial",
            ["Python", "SQL", "Docker"],
            apply_url="https://jobs.example/partial",
        )
        self._add_job(
            "complete",
            ["Python", "SQL"],
            apply_url="https://jobs.example/complete",
        )

        first_run = opportunity_matching.recommend_opportunities(
            self.client, "student-1"
        )
        second_run = opportunity_matching.recommend_opportunities(
            self.client, "student-1"
        )

        self.assertEqual(
            [(match.job_id, match.match_score) for match in first_run],
            [("complete", 100.0), ("partial", 66.7)],
        )
        self.assertEqual(
            [(match.job_id, match.match_score) for match in first_run],
            [(match.job_id, match.match_score) for match in second_run],
        )

    def test_preferences_only_affect_score_when_provided(self):
        self._add_student_skills("Python")
        self._add_job("job-1", ["Python"])

        no_preferences = opportunity_matching.recommend_opportunities(
            self.client, "student-1"
        )
        preferred = opportunity_matching.recommend_opportunities(
            self.client,
            "student-1",
            location="Remote",
            job_type="internship",
        )

        self.assertEqual(no_preferences[0].match_score, 100.0)
        self.assertEqual(preferred[0].match_score, 100.0)
        self.assertEqual(
            preferred[0].formula_version,
            opportunity_matching.FORMULA_VERSION,
        )


class ProfileSkillSyncTests(unittest.TestCase):
    def test_saving_profile_removes_skills_from_previous_resume(self):
        client = FakeClient({
            "profiles": [],
            "skills": [
                {"id": "skill-python", "name": "Python"},
                {"id": "skill-rust", "name": "Rust"},
            ],
            "student_skills": [
                {"student_id": "student-1", "skill_id": "skill-python"},
                {"student_id": "student-1", "skill_id": "skill-rust"},
                {"student_id": "student-2", "skill_id": "skill-rust"},
            ],
            "projects": [],
        })
        profile = StudentProfile(
            full_name="Candidate",
            skills=[
                Skill(
                    name="Python",
                    category="Technical",
                    proficiency="Intermediate",
                    confidence=0.9,
                    evidence="Resume project",
                )
            ],
            projects=[],
        )

        save_student_profile(client, "student-1", profile)

        self.assertEqual(
            {
                (row["student_id"], row["skill_id"])
                for row in client.tables["student_skills"]
            },
            {("student-1", "skill-python"), ("student-2", "skill-rust")},
        )


class CandidateMatchInvalidationTests(unittest.TestCase):
    def test_saving_no_matches_removes_persisted_recommendations(self):
        client = FakeClient({
            "opportunity_matches": [
                {"student_id": "student-1", "job_id": "old-job"},
                {"student_id": "student-2", "job_id": "other-student-job"},
            ]
        })

        saved = save_opportunity_matches(client, "student-1", [])

        self.assertEqual(saved, 0)
        self.assertEqual(
            client.tables["opportunity_matches"],
            [{"student_id": "student-2", "job_id": "other-student-job"}],
        )

    def test_saving_new_results_removes_stale_recommendations(self):
        client = FakeClient({
            "opportunity_matches": [
                {"student_id": "student-1", "job_id": "stale-job"},
                {"student_id": "student-2", "job_id": "other-student-job"},
            ]
        })
        recommendation = RecommendedOpportunity(
            job_id="current-job",
            title="Python Developer",
            company="Example",
            apply_url="https://jobs.example/apply",
            match_score=100,
            matched_skills=["Python"],
            missing_skills=[],
            reason="Matched Python.",
            formula_version="coverage-location-type-v3",
        )

        saved = save_opportunity_matches(
            client, "student-1", [recommendation]
        )

        self.assertEqual(saved, 1)
        student_matches = [
            row for row in client.tables["opportunity_matches"]
            if row["student_id"] == "student-1"
        ]
        self.assertEqual(
            [row["job_id"] for row in student_matches],
            ["current-job"],
        )
        self.assertTrue(
            any(
                row["student_id"] == "student-2"
                for row in client.tables["opportunity_matches"]
            )
        )


if __name__ == "__main__":
    unittest.main()
