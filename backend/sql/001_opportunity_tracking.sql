alter table public.jobs
add column if not exists external_id text,
add column if not exists content_hash text,
add column if not exists eligibility jsonb,
add column if not exists last_seen_at timestamptz default now(),
add column if not exists is_active boolean default true,
add column if not exists updated_at timestamptz default now();

create unique index if not exists jobs_source_external_id_unique
on public.jobs(source, external_id);

create index if not exists jobs_active_source_index
on public.jobs(source, is_active);
