# SkillSetu Database Migrations

This directory contains the numbered SQL migrations for SkillSetu in exact execution order.
Execute these sequentially against your Supabase or PostgreSQL database via the Supabase SQL Editor.

## Apply Order

1. **`000_base_schema.sql`**
   - Creates fundamental core tables: `profiles`, `skills`, `student_skills`, `projects`, `jobs`, and `job_skills`.
   - Sets up initial Row Level Security (RLS) policies for user profiles, student skills, and projects.

2. **`001_opportunity_tracking.sql`**
   - Adds indexes and tracking fields (`last_seen_at`, `is_active`) on the `jobs` table for job ingestion synchronization.

3. **`002_opportunity_rls.sql`**
   - Configures read policies on `jobs` and `job_skills` for authenticated users.

4. **`003_candidate_state.sql`**
   - Creates `student_preferences` (for storing user filter choices) and `opportunity_matches` (for candidate match score persistence).
   - Establishes cascading foreign keys to `profiles` and `jobs`.

5. **`004_multi_resume.sql`**
   - Creates `student_resumes` table supporting multiple named resumes/profiles (e.g. "Full-Stack Dev", "AI/ML Engineer") and active resume toggling.

6. **`005_learning_progress.sql`**
   - Creates `student_learning_progress` table tracking per-skill milestones (`not_started`, `in_progress`, `completed`) and verification evidence.

## How to Apply

In the Supabase Dashboard:
1. Navigate to **SQL Editor**.
2. Open each file from `000` through `005` in order.
3. Click **Run** for each migration.
4. Verify table existence by running `python backend/verify_db.py`.
