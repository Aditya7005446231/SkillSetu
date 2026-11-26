create table if not exists public.student_learning_progress (
    student_id uuid references public.profiles(id) on delete cascade not null,
    skill_key text not null,
    skill_name text not null,
    status text not null
        check (status in ('not_started', 'in_progress', 'completed')),
    evidence_url text,
    evidence_note text not null default '',
    updated_at timestamptz not null default now(),
    primary key (student_id, skill_key),
    check (
        status <> 'completed'
        or evidence_url is not null
        or length(btrim(evidence_note)) >= 20
    )
);

alter table public.student_learning_progress enable row level security;

drop policy if exists "Students manage their own learning progress"
on public.student_learning_progress;
create policy "Students manage their own learning progress"
on public.student_learning_progress
for all
to authenticated
using (auth.uid() = student_id)
with check (auth.uid() = student_id);
