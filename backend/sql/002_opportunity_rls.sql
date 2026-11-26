-- Development policies for the authenticated opportunity sync endpoint.
-- Replace these with an admin/service-role workflow before production.

alter table public.jobs enable row level security;
alter table public.job_skills enable row level security;

drop policy if exists "Authenticated users can view jobs" on public.jobs;
drop policy if exists "Authenticated users can insert jobs" on public.jobs;
drop policy if exists "Authenticated users can update jobs" on public.jobs;
drop policy if exists "Authenticated users can view job skills" on public.job_skills;
drop policy if exists "Authenticated users can insert job skills" on public.job_skills;
drop policy if exists "Authenticated users can update job skills" on public.job_skills;

create policy "Authenticated users can view jobs"
on public.jobs for select
to authenticated
using (true);

create policy "Authenticated users can insert jobs"
on public.jobs for insert
to authenticated
with check (true);

create policy "Authenticated users can update jobs"
on public.jobs for update
to authenticated
using (true)
with check (true);

create policy "Authenticated users can view job skills"
on public.job_skills for select
to authenticated
using (true);

create policy "Authenticated users can insert job skills"
on public.job_skills for insert
to authenticated
with check (true);

create policy "Authenticated users can update job skills"
on public.job_skills for update
to authenticated
using (true)
with check (true);
