-- Migration: Candidate State & Student Preferences

-- 1. Student Preferences Table
create table if not exists public.student_preferences (
    student_id uuid references public.profiles(id) on delete cascade primary key,
    preferred_location text default '',
    remote_only boolean default false,
    preferred_job_type text default '',
    preferred_skills jsonb default '[]'::jsonb,
    target_role text default '',
    minimum_score numeric default 0,
    updated_at timestamptz default now()
);

-- 2. Opportunity Matches (Candidate State) Table
create table if not exists public.opportunity_matches (
    id uuid default gen_random_uuid() primary key,
    student_id uuid references public.profiles(id) on delete cascade not null,
    job_id bigint references public.jobs(id) on delete cascade not null,
    match_score numeric not null,
    matched_skills jsonb default '[]'::jsonb,
    missing_skills jsonb default '[]'::jsonb,
    related_gap_skills jsonb default '{}'::jsonb,
    reason text default '',
    formula_version text default 'coverage-location-type-v2-rag',
    calculated_at timestamptz default now(),
    unique(student_id, job_id)
);

create index if not exists idx_opportunity_matches_student
on public.opportunity_matches(student_id, match_score desc);

-- RLS Configuration
alter table public.student_preferences enable row level security;
alter table public.opportunity_matches enable row level security;

-- Policies for student_preferences
drop policy if exists "Students can manage own preferences" on public.student_preferences;
create policy "Students can manage own preferences"
on public.student_preferences
for all
to authenticated
using (auth.uid() = student_id)
with check (auth.uid() = student_id);

-- Policies for opportunity_matches
drop policy if exists "Students can view own opportunity matches" on public.opportunity_matches;
create policy "Students can view own opportunity matches"
on public.opportunity_matches
for select
to authenticated
using (auth.uid() = student_id);

drop policy if exists "Students can insert/update opportunity matches" on public.opportunity_matches;
create policy "Students can insert/update opportunity matches"
on public.opportunity_matches
for all
to authenticated
using (auth.uid() = student_id)
with check (auth.uid() = student_id);
