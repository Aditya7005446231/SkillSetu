"""Deterministic, job-grounded learning roadmaps."""

from collections import defaultdict
from typing import Any

from .skill_framework_rag import normalize_skill

MAX_ROADMAP_JOBS = 5


def build_learning_roadmaps(
    recommendations: list[Any],
    student_skills: list[str],
    framework_documents: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build per-job roadmaps plus skill gaps shared across top recommendations."""
    jobs = [_recommendation_dict(item) for item in recommendations[:MAX_ROADMAP_JOBS]]
    framework = {
        _skill_key(document.get("title") or document.get("name", "")): document
        for document in framework_documents
        if document.get("title") or document.get("name")
    }
    known_skills = {
        _skill_key(skill) for skill in student_skills if _skill_key(skill)
    }

    target_roadmaps = [
        _build_target_roadmap(job, known_skills, framework)
        for job in jobs
    ]
    shared_core = _build_shared_core(jobs, known_skills, framework)

    return {
        "available_jobs": [
            {
                "job_id": job["job_id"],
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "job_type": job["job_type"],
                "match_score": job["match_score"],
            }
            for job in jobs
        ],
        "target_roadmaps": target_roadmaps,
        "shared_core": shared_core,
    }


def _recommendation_dict(recommendation: Any) -> dict[str, Any]:
    if isinstance(recommendation, dict):
        record = recommendation
    else:
        record = recommendation.model_dump()

    return {
        "job_id": str(record.get("job_id") or ""),
        "title": str(record.get("title") or "Target role"),
        "company": str(record.get("company") or ""),
        "location": str(record.get("location") or ""),
        "job_type": str(record.get("job_type") or ""),
        "match_score": float(record.get("match_score") or 0),
        "missing_skills": _unique_skills(record.get("missing_skills") or []),
    }


def _unique_skills(skills: list[str]) -> list[str]:
    unique: dict[str, str] = {}
    for skill in skills:
        canonical = normalize_skill(str(skill)).strip()
        if canonical:
            unique.setdefault(_skill_key(canonical), canonical)
    return list(unique.values())


def _skill_key(skill: str) -> str:
    return normalize_skill(str(skill)).strip().casefold()


def _build_target_roadmap(
    job: dict[str, Any],
    known_skills: set[str],
    framework: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    gaps = job["missing_skills"]
    role = job["title"]
    direct_requirements = [
        {
            "skill": skill,
            "reason": f"Required by {role}.",
            "roles": [role],
            "occurrences": 1,
        }
        for skill in gaps
    ]
    steps = _build_steps(direct_requirements, known_skills, framework)

    return {
        "job_id": job["job_id"],
        "title": job["title"],
        "company": job["company"],
        "location": job["location"],
        "job_type": job["job_type"],
        "match_score": job["match_score"],
        "missing_skills": gaps,
        "steps": steps,
        "project": _project_action(gaps, [role]) if gaps else "",
        "message": (
            "No required skill gaps were identified for this role."
            if not gaps
            else ""
        ),
    }


def _build_shared_core(
    jobs: list[dict[str, Any]],
    known_skills: set[str],
    framework: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    gap_sources: dict[str, dict[str, Any]] = {}
    for job in jobs:
        for skill in job["missing_skills"]:
            key = _skill_key(skill)
            source = gap_sources.setdefault(
                key,
                {
                    "skill": skill,
                    "roles": [],
                    "score_total": 0.0,
                    "occurrences": 0,
                },
            )
            source["occurrences"] += 1
            source["score_total"] += job["match_score"]
            if job["title"] not in source["roles"]:
                source["roles"].append(job["title"])

    # A shared-core skill must appear in at least two distinct recommended jobs.
    shared = [
        source
        for source in gap_sources.values()
        if source["occurrences"] >= 2
    ]
    shared.sort(
        key=lambda item: (
            -item["occurrences"],
            -item["score_total"],
            item["skill"].casefold(),
        )
    )
    requirements = [
        {
            "skill": item["skill"],
            "reason": (
                f"Missing from {item['occurrences']} of {len(jobs)} top "
                f"recommended roles: {', '.join(item['roles'])}."
            ),
            "roles": item["roles"],
            "occurrences": item["occurrences"],
        }
        for item in shared
    ]
    steps = _build_steps(requirements, known_skills, framework)

    return {
        "source_job_count": len(jobs),
        "skills": [
            {
                "name": item["skill"],
                "occurrences": item["occurrences"],
                "role_count": len(item["roles"]),
                "roles": item["roles"],
            }
            for item in shared
        ],
        "steps": steps,
        "project": (
            _project_action(
                [item["skill"] for item in shared],
                [job["title"] for job in jobs],
            )
            if shared
            else ""
        ),
        "message": (
            "No skill gap appears in two or more recommended roles yet. "
            "Choose a target role for a focused roadmap."
            if not shared
            else ""
        ),
    }


def _build_steps(
    direct_requirements: list[dict[str, Any]],
    known_skills: set[str],
    framework: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    direct_by_key: dict[str, dict[str, Any]] = {}
    dependencies: dict[str, set[str]] = defaultdict(set)
    display_names: dict[str, str] = {}
    pending: list[str] = []

    for requirement in direct_requirements:
        skill = requirement["skill"]
        key = _skill_key(skill)
        if not key or key in known_skills:
            continue
        direct_by_key[key] = requirement
        display_names[key] = skill
        pending.append(skill)

    processed: set[str] = set()
    while pending:
        skill = pending.pop()
        key = _skill_key(skill)
        if not key or key in processed or key in known_skills:
            continue
        processed.add(key)
        document = framework.get(key, {})
        display_names.setdefault(
            key,
            str(document.get("title") or document.get("name") or skill),
        )

        for raw_prerequisite in document.get("prerequisites") or []:
            prerequisite = normalize_skill(str(raw_prerequisite)).strip()
            prerequisite_key = _skill_key(prerequisite)
            if not prerequisite_key or prerequisite_key in known_skills:
                continue
            dependencies[key].add(prerequisite_key)
            display_names.setdefault(prerequisite_key, prerequisite)
            if prerequisite_key not in processed:
                pending.append(prerequisite)

    remaining = set(processed)
    ordered_keys: list[str] = []
    prerequisite_keys = {
        prerequisite
        for prerequisites in dependencies.values()
        for prerequisite in prerequisites
    }
    while remaining:
        ready = sorted(
            (
                key
                for key in remaining
                if not dependencies[key].intersection(remaining)
            ),
            key=lambda key: (
                key not in prerequisite_keys,
                display_names[key].casefold(),
            ),
        )
        if not ready:
            raise ValueError("Skill framework prerequisites contain a cycle.")
        next_skill = ready[0]
        ordered_keys.append(next_skill)
        remaining.remove(next_skill)

    dependents: dict[str, list[str]] = defaultdict(list)
    for skill_key, prerequisite_keys in dependencies.items():
        for prerequisite_key in prerequisite_keys:
            dependents[prerequisite_key].append(display_names[skill_key])

    steps = []
    for index, key in enumerate(ordered_keys, start=1):
        skill = display_names[key]
        requirement = direct_by_key.get(key)
        if requirement:
            reason = requirement["reason"]
            action = f"Practice {skill} in a task aligned with {', '.join(requirement['roles'])}."
            kind = "job_requirement"
        else:
            dependent_skills = sorted(set(dependents[key]), key=str.casefold)
            reason = (
                f"Framework prerequisite for {', '.join(dependent_skills)}; "
                "not found in the active skill profile."
            )
            action = (
                f"Learn and practice {skill} before moving on to "
                f"{', '.join(dependent_skills)}."
            )
            kind = "prerequisite"
        document = framework.get(key, {})
        learning_task = (
            f"Build a small {skill} feature related to {', '.join(requirement['roles'])}."
            if requirement
            else f"Complete a focused {skill} exercise before continuing to "
            f"{', '.join(sorted(set(dependents[key]), key=str.casefold))}."
        )

        steps.append(
            {
                "order": index,
                "skill": skill,
                "kind": kind,
                "reason": reason,
                "action": action,
                "description": str(document.get("description") or ""),
                "learning_task": learning_task,
                "acceptance_criteria": [
                    f"Create an inspectable artifact that demonstrates {skill}.",
                    "Document what you built and how you verified it.",
                ],
                "prerequisites": sorted(
                    (
                        display_names[dependency]
                        for dependency in dependencies[key]
                    ),
                    key=str.casefold,
                ),
            }
        )
    return steps


def _project_action(skills: list[str], roles: list[str]) -> str:
    unique_skills = list(dict.fromkeys(skills))
    unique_roles = list(dict.fromkeys(roles))
    if not unique_skills:
        return ""
    role_context = ", ".join(unique_roles[:3])
    return (
        f"Build a small portfolio project demonstrating "
        f"{', '.join(unique_skills)}"
        + (f" in a context relevant to {role_context}." if role_context else ".")
        + " Document what you built so it can be verified."
    )
