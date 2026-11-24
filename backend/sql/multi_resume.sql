-- SQL Migration for Multi-Resume Profiles and Manual Onboarding
-- Enables students to save multiple labeled resumes (e.g. "Full-Stack Dev", "AI/ML Engineer")
-- and manage custom manual skills/preferences per resume.

create table if not exists public.student_resumes (
    id uuid primary key default gen_random_uuid(),
    student_id uuid not null,
    label varchar(100) not null default 'Primary Resume',
    filename varchar(255) not null default 'manual_profile.pdf',
    career_goal text default '',
    target_role varchar(120) default '',
    raw_text text default '',
    is_active boolean default false,
    parsed_profile jsonb not null default '{}'::jsonb,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

create index if not exists idx_student_resumes_student on public.student_resumes(student_id);
create index if not exists idx_student_resumes_active on public.student_resumes(student_id, is_active);

-- Enable RLS
alter table public.student_resumes enable row level security;

-- Student RLS policies
drop policy if exists "Students can manage own resumes" on public.student_resumes;
create policy "Students can manage own resumes"
    on public.student_resumes
    for all
    to authenticated
    using (student_id = auth.uid())
    with check (student_id = auth.uid());
