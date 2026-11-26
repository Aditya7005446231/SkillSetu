# Student-Job Matching Agent Plan

## Goal

Create a matching agent that compares an authenticated student's extracted
skills with active job requirements and returns transparent, ranked job
recommendations.

The agent should work as a reusable backend service rather than being embedded
inside an API route or the React frontend.

## Scope

### Included

- Load the student's profile and skills from Supabase.
- Load active jobs and their required skills.
- Match exact and normalized skill names.
- Apply location and employment-type preferences.
- Calculate a clear match score.
- Return matched and missing skills.
- Rank opportunities by relevance.
- Store or recalculate recommendation results.
- Expose one authenticated recommendations endpoint.
- Redirect students to the original external application URL.

### Not included yet

- RAG over institutional or national skill frameworks.
- Conversational preference collection.
- Salary prediction.
- AI-generated explanations.
- Multi-agent planner-executor orchestration.
- Fairness monitoring dashboards.
- Personalization based on protected personal attributes.

## Current data available

The existing project already stores:

- Student profile and resume-derived information.
- Student skills and `student_skills`.
- Active jobs and normalized job metadata.
- Job skills in `job_skills`.
- Job location and job type.
- Original `apply_url`.
- Job content hashes and active status.

The current matching implementation must not assume that every job's skills
are complete or perfectly normalized.

## Proposed architecture

```text
Student resume
    -> Resume profiling
    -> student_skills

JSearch
    -> Job normalization
    -> Groq requirement extraction
    -> job_skills

Matching agent
    -> Load student skills
    -> Load active jobs
    -> Apply preferences
    -> Score and rank jobs
    -> Return recommendations
```

## Matching formula

Use a deterministic, explainable score initially.

```text
matched_skills = student_skills intersect job_required_skills
coverage_score = matched_skill_count / required_skill_count
```

For a more useful initial ranking, combine coverage with:

```text
required skill importance
student skill proficiency, if available
location match
job-type match
```

Recommended initial formula:

```text
score =
  0.80 * required_skill_coverage
  + 0.10 * location_score
  + 0.10 * job_type_score
```

The score must be returned as a number from `0` to `100`.
When a student has not specified a location or job-type preference, omit that
dimension and proportionally normalize the remaining weights. Do not award
preference points simply because a preference was not provided.

Only recommend jobs with at least one matched skill, extracted job
requirements, and a valid HTTP(S) application URL. If the student has no
recognized skills, return no recommendations and show a clear empty state.

Example:

```text
Student skills:
Python, SQL, FastAPI

Job skills:
Python, Django, PostgreSQL, Docker

Matched:
Python

Missing:
Django, PostgreSQL, Docker

Required skill coverage:
25%

Final recommendation score:
For a location/job-type match, approximately 30%
```

The formula should be versioned and visible in code so it can be tested and
changed later.

## Skill normalization

Before comparison, normalize both student and job skill names.

Examples:

```text
"PostgreSQL"  -> "postgresql"
"Postgres"    -> "postgresql"
"Fast API"    -> "fastapi"
"ReactJS"     -> "react"
"Node.js"     -> "nodejs"
"JS"          -> "javascript"
```

Normalization should use a documented alias table initially. It should not
invent equivalences with no evidence.

The matching result may later include skill aliases and confidence levels.

## Filters

Apply filters before ranking or store them as ranking penalties.

Initial filters:

- Active jobs only
- Country: India
- Preferred cities
- Remote-only or on-site preference
- Full-time, internship, part-time, contract, or other
- Optional minimum match score

Location matching must distinguish:

- Exact city match
- State/country match
- Remote jobs
- Unknown locations

Unknown locations should not automatically be excluded unless the student
explicitly requires a known location.

## Supabase schema

Create an `opportunity_matches` table:

```sql
student_id uuid not null
job_id uuid not null
match_score numeric not null
matched_skills jsonb not null default '[]'
missing_skills jsonb not null default '[]'
location_score numeric not null default 0
job_type_score numeric not null default 0
formula_version text not null
calculated_at timestamptz not null default now()
```

Recommended constraints:

```text
primary key (student_id, job_id)
foreign key student_id -> auth.users(id)
foreign key job_id -> public.jobs(id)
match_score between 0 and 100
```

The table can be recalculated during synchronization or when the student's
profile changes.

## Backend components

### 1. Matching schema

Add a Pydantic response model containing:

- Job ID
- Title
- Company
- Location
- Job type
- Application URL
- Match score
- Matched skills
- Missing skills
- Recommendation reason

### 2. Matching service

Create:

```text
backend/app/services/opportunity_matching.py
```

Responsibilities:

1. Load student skills.
2. Load active job requirements.
3. Normalize skill names.
4. Apply preferences and filters.
5. Calculate match scores.
6. Rank jobs.
7. Return explainable results.

### 3. Matching persistence

Create:

```text
backend/app/services/matching_persistence.py
```

Responsibilities:

- Upsert one recommendation row.
- Update existing scores when requirements or student skills change.
- Remove or deactivate stale recommendations.
- Keep calculation timestamps for monitoring.

### 4. API endpoint

Add:

```text
GET /api/opportunities/recommended
```

Optional query parameters:

```text
location
job_type
remote
minimum_score
limit
```

The endpoint must use the authenticated student ID and must not accept an
arbitrary `student_id` from the request.

## Ranking behavior

Sort by:

1. Match score descending
2. Job type preference match
3. Location preference match
4. Recent posting or last seen descending

Do not rank exclusively by skill count. A 2/2 skill match should not
automatically beat a 8/10 skill match unless the formula explicitly rewards
it.

## Transparency

Each result should explain why it matched:

```text
"Matched Python and SQL. Missing Django and Docker."
```

The frontend should show both:

- Skills the student already has.
- Skills that require development.

The original application URL must remain visible and function as the final
action.

## Learning roadmaps

Roadmaps are derived from recommendation data and the active student profile;
they are not generated from a generic role template.

- A target-job roadmap contains that job's missing required skills.
- Framework prerequisites absent from the active profile are added before the
  skills that depend on them, using the framework's explicit prerequisite
  relationships.
- A shared-core roadmap includes only skills missing from at least two of the
  top five recommended jobs. Gaps are prioritized by frequency, then match
  scores, with skill name as a deterministic tie-breaker.
- Each step includes a role-aligned practice task and a small definition of
  done. Students can save progress and submit a project URL or written evidence.
- Progress is a student-submitted claim, not an automatic skill verification;
  submitting it does not change recommendation scores or the active profile.
- Apply `backend/sql/learning_progress.sql` to enable progress persistence.
- If there are no eligible recommendations, do not invent a roadmap.
- "Missing" means no evidence was found in the active profile; it is not proof
  that the student cannot perform the skill.

## Validation rules

Before saving a recommendation:

- Job must be active.
- Job must have a valid application URL.
- Student must have at least one recognized skill.
- Match score must be between 0 and 100.
- `matched_skills` must not contain missing skills.
- Duplicate `(student_id, job_id)` matches must be upserted, not inserted twice.

If a student has no skills, return a clear response rather than ranking every
job as a low match.

## Testing plan

### Unit tests

- Exact skill match
- Missing skill
- Case and whitespace normalization
- Known skill aliases
- Internship/full-time classification
- Remote location
- Empty student skill list
- Empty job skill list
- Duplicate recommendation upsert

### Service tests

- Student has 2 of 4 required skills.
- Remote preference with unknown location.
- Location mismatch penalty.
- Job-type mismatch penalty.
- Correct descending ranking.
- Stale recommendations are updated or removed.

### API tests

- Request without authentication returns `401`.
- Student cannot request another student's recommendations.
- Invalid filters return `422`.
- Active jobs are returned.
- Inactive jobs are excluded.
- Application URL is preserved.

### Live integration test

Run one controlled sync and verify:

```text
JSearch returns jobs
→ Jobs are active
→ Job skills exist
→ Student skills exist
→ Recommendations are created
→ Ranking is deterministic
→ Apply URLs are valid
```

## Implementation phases

### Phase 1: Deterministic matching

- Add skill normalization.
- Create matching service.
- Add authenticated recommendation endpoint.
- Return matched and missing skills.

### Phase 2: Persistence

- Create `opportunity_matches`.
- Upsert recommendations.
- Recalculate after profile or sync changes.

### Phase 3: Preferences

- Add location and job-type filters.
- Add remote preference.
- Store student preference state.

### Phase 4: Frontend

- Create a recommendations page or enhance the Opportunities page.
- Show match score and matched/missing skills.
- Add filters.
- Link directly to the original application page.

### Phase 5: Quality and monitoring

- Record formula version and calculation timestamp.
- Track empty-result rates.
- Track matching latency.
- Compare rankings across demographic groups only when the system
  explicitly stores appropriate and authorized audit data.
- Prevent protected attributes from affecting ranking.

## Success criteria

The first working version is complete when:

1. An authenticated student receives ranked recommendations.
2. Recommendations are based only on active jobs.
3. Match scores are reproducible.
4. Matched and missing skills are visible.
5. Location and job type can be filtered.
6. Results persist in Supabase.
7. The original external application link works.
8. Another student cannot read or manipulate the student's recommendations.

## Immediate next implementation

Start with a read-only recommendation endpoint and deterministic matching
logic. Do not add RAG or conversational orchestration until the core matching
flow is tested end to end.
