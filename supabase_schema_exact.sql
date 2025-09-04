-- =====================================================
-- EXACT SCHEMA per user's definitions + minimal runtime plumbing
-- Run this in your Supabase project's SQL Editor
-- Project: rmweyfpxxnonlojspbkn
-- =====================================================

-- Extensions (ensure available)
create extension if not exists pgcrypto;

-- =========================
-- Tables (exact definitions)
-- =========================

create table if not exists public.user_profiles (
  id uuid not null default gen_random_uuid(),
  user_id uuid not null,
  email text not null,
  first_name text not null,
  last_name text not null,
  phone text null,
  country text null,
  age integer null,
  profile_picture_url text null,
  created_at timestamp with time zone null default now(),
  updated_at timestamp with time zone null default now(),
  constraint user_profiles_pkey primary key (id),
  constraint user_profiles_user_id_key unique (user_id),
  constraint user_profiles_user_id_fkey foreign key (user_id) references auth.users (id) on delete cascade,
  constraint user_profiles_age_check check (((age >= 1) and (age <= 120)))
) tablespace pg_default;

create index if not exists idx_user_profiles_user_id on public.user_profiles using btree (user_id) tablespace pg_default;
create index if not exists idx_user_profiles_email on public.user_profiles using btree (email) tablespace pg_default;
create index if not exists idx_user_profiles_created_at on public.user_profiles using btree (created_at) tablespace pg_default;

create table if not exists public.admin_users (
  id uuid not null default gen_random_uuid(),
  user_id uuid null,
  is_admin boolean null default false,
  created_at timestamp with time zone null default now(),
  updated_at timestamp with time zone null default now(),
  constraint admin_users_pkey primary key (id),
  constraint admin_users_user_id_fkey foreign key (user_id) references auth.users (id) on delete cascade
) tablespace pg_default;

create index if not exists idx_admin_users_user_id on public.admin_users using btree (user_id) tablespace pg_default;
create index if not exists idx_admin_users_is_admin on public.admin_users using btree (is_admin) tablespace pg_default;
create unique index if not exists uq_admin_users_user_id on public.admin_users using btree (user_id) tablespace pg_default;

-- =========================
-- Minimal helper functions
-- =========================

create or replace function public.update_updated_at_column()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create or replace function public.set_user_email()
returns trigger as $$
begin
  if new.email is null or new.email = '' then
    select email into new.email from auth.users where id = new.user_id;
  end if;
  return new;
end;
$$ language plpgsql;

-- =========================
-- Triggers (exact names as provided)
-- =========================

drop trigger if exists set_user_profiles_email on public.user_profiles;
create trigger set_user_profiles_email before insert or update on public.user_profiles
for each row execute function public.set_user_email();

drop trigger if exists update_user_profiles_updated_at on public.user_profiles;
create trigger update_user_profiles_updated_at before update on public.user_profiles
for each row execute function public.update_updated_at_column();

drop trigger if exists update_admin_users_updated_at on public.admin_users;
create trigger update_admin_users_updated_at before update on public.admin_users
for each row execute function public.update_updated_at_column();

-- =========================
-- RLS (minimal policies so anon/auth can operate via client)
-- =========================

alter table public.user_profiles enable row level security;
alter table public.admin_users enable row level security;

-- Profiles: users can manage their own row by user_id
do $$
begin
  if not exists (
    select 1 from pg_policies
    where schemaname = 'public' and tablename = 'user_profiles' and policyname = 'Users can view own profile'
  ) then
    create policy "Users can view own profile" on public.user_profiles for select using (auth.uid() = user_id);
  end if;
  if not exists (
    select 1 from pg_policies
    where schemaname = 'public' and tablename = 'user_profiles' and policyname = 'Users can insert own profile'
  ) then
    create policy "Users can insert own profile" on public.user_profiles for insert with check (auth.uid() = user_id);
  end if;
  if not exists (
    select 1 from pg_policies
    where schemaname = 'public' and tablename = 'user_profiles' and policyname = 'Users can update own profile'
  ) then
    create policy "Users can update own profile" on public.user_profiles for update using (auth.uid() = user_id);
  end if;
  if not exists (
    select 1 from pg_policies
    where schemaname = 'public' and tablename = 'user_profiles' and policyname = 'Users can delete own profile'
  ) then
    create policy "Users can delete own profile" on public.user_profiles for delete using (auth.uid() = user_id);
  end if;
end $$;

-- Admins table: everyone can insert their own default row via trigger; users can view their own; admins can view all
do $$
begin
  if not exists (
    select 1 from pg_policies
    where schemaname = 'public' and tablename = 'admin_users' and policyname = 'Users can view own admin row'
  ) then
    create policy "Users can view own admin row" on public.admin_users for select using (auth.uid() = user_id);
  end if;
  if not exists (
    select 1 from pg_policies
    where schemaname = 'public' and tablename = 'admin_users' and policyname = 'Users can insert own admin row'
  ) then
    create policy "Users can insert own admin row" on public.admin_users for insert with check (auth.uid() = user_id);
  end if;
end $$;

-- =========================
-- Auto-provision rows on signup from raw_user_meta_data
-- =========================

create or replace function public.handle_new_user()
returns trigger as $$
begin
  -- create admin row (default false)
  insert into public.admin_users (user_id, is_admin) values (new.id, false)
  on conflict (user_id) do nothing;

  -- create profile row using metadata
  insert into public.user_profiles (
    user_id, email, first_name, last_name, phone
  ) values (
    new.id,
    new.email,
    coalesce(new.raw_user_meta_data->>'firstName', ''),
    coalesce(new.raw_user_meta_data->>'lastName', ''),
    coalesce(new.raw_user_meta_data->>'phone', '')
  ) on conflict (user_id) do nothing;

  return new;
end;
$$ language plpgsql security definer;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- =========================
-- Grants (minimal)
-- =========================

grant usage on schema public to anon, authenticated;
grant select, insert, update, delete on public.user_profiles to authenticated;
grant select, insert on public.admin_users to authenticated;


