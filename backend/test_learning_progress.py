"""Tests for persisted, evidence-backed student learning progress."""

import sys
from pathlib import Path
import unittest
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pydantic import ValidationError

from app.schemas.learning_progress import LearningProgressUpdate
from app.services.learning_progress import (
    get_student_learning_progress,
    save_student_learning_progress,
)


class FakeQuery:
    def __init__(self, client, table_name):
        self.client = client
        self.table_name = table_name
        self.filters = {}
        self.payload = None

    def select(self, *_args):
        return self

    def eq(self, key, value):
        self.filters[key] = value
        return self

    def upsert(self, payload, on_conflict=None):
        self.payload = payload
        self.conflict_keys = [key.strip() for key in on_conflict.split(",")]
        return self

    def execute(self):
        rows = self.client.tables.setdefault(self.table_name, [])
        if self.payload is not None:
            existing = next(
                (
                    row
                    for row in rows
                    if all(
                        row.get(key) == self.payload.get(key)
                        for key in self.conflict_keys
                    )
                ),
                None,
            )
            if existing:
                existing.update(self.payload)
                return SimpleNamespace(data=[existing])
            rows.append(dict(self.payload))
            return SimpleNamespace(data=[rows[-1]])

        selected = [
            row
            for row in rows
            if all(row.get(key) == value for key, value in self.filters.items())
        ]
        return SimpleNamespace(data=selected)


class FakeClient:
    def __init__(self):
        self.tables = {"student_learning_progress": []}

    def table(self, name):
        return FakeQuery(self, name)


class LearningProgressTests(unittest.TestCase):
    def setUp(self):
        self.client = FakeClient()
        self.normalize_patch = patch(
            "app.services.learning_progress.normalize_skill",
            side_effect=lambda skill: {
                "reactjs": "React",
                "react": "React",
            }.get(skill.strip().lower(), skill.strip()),
        )
        self.normalize_patch.start()
        self.addCleanup(self.normalize_patch.stop)

    def test_completion_requires_a_url_or_substantial_evidence_note(self):
        with self.assertRaises(ValidationError):
            LearningProgressUpdate(
                skill_name="React",
                status="completed",
                evidence_note="I built a small app",
            )

        update = LearningProgressUpdate(
            skill_name="React",
            status="completed",
            evidence_note="Built and tested a responsive React task board.",
        )
        self.assertEqual(update.status, "completed")

    def test_progress_upserts_by_student_and_canonical_skill(self):
        first = LearningProgressUpdate(
            skill_name="ReactJS",
            status="in_progress",
        )
        completed = LearningProgressUpdate(
            skill_name="React",
            status="completed",
            evidence_note="Built and tested a responsive React task board.",
        )

        save_student_learning_progress(self.client, "student-1", first)
        save_student_learning_progress(self.client, "student-1", completed)
        save_student_learning_progress(self.client, "student-2", first)

        rows = self.client.tables["student_learning_progress"]
        self.assertEqual(len(rows), 2)
        self.assertEqual(
            {
                (row["student_id"], row["skill_key"], row["status"])
                for row in rows
            },
            {
                ("student-1", "react", "completed"),
                ("student-2", "react", "in_progress"),
            },
        )

    def test_read_only_returns_only_the_requested_students_progress(self):
        self.client.tables["student_learning_progress"] = [
            {"student_id": "student-1", "skill_name": "Python"},
            {"student_id": "student-2", "skill_name": "React"},
        ]

        progress = get_student_learning_progress(self.client, "student-1")

        self.assertEqual([item["skill_name"] for item in progress], ["Python"])


if __name__ == "__main__":
    unittest.main()
