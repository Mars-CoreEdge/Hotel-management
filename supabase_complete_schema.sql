-- ===========================================
-- COMPLETE SUPABASE SCHEMA SETUP
-- ===========================================

-- First, create the required functions if they don't exist
-- Function to update the updated_at column
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Function to set user email from auth.users
CREATE OR REPLACE FUNCTION set_user_email()
RETURNS TRIGGER AS $$
BEGIN
    -- Get email from auth.users table
    SELECT email INTO NEW.email
    FROM auth.users
    WHERE id = NEW.user_id;
    
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Function to handle new user signup (creates profile and admin record)
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert into user_profiles
    INSERT INTO public.user_profiles (user_id, email, first_name, last_name)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'first_name', ''),
        COALESCE(NEW.raw_user_meta_data->>'last_name', '')
    );
    
    -- Insert into admin_users (default to false)
    INSERT INTO public.admin_users (user_id, is_admin)
    VALUES (NEW.id, false);
    
    RETURN NEW;
END;
$$ language 'plpgsql';

-- ===========================================
-- USER PROFILES TABLE
-- ===========================================

-- Drop table if exists (for clean setup)
DROP TABLE IF EXISTS public.user_profiles CASCADE;

-- Create user_profiles table
CREATE TABLE public.user_profiles (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL,
    email text NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL,
    phone text NULL,
    country text NULL,
    age integer NULL,
    profile_picture_url text NULL,
    created_at timestamp with time zone NULL DEFAULT now(),
    updated_at timestamp with time zone NULL DEFAULT now(),
    CONSTRAINT user_profiles_pkey PRIMARY KEY (id),
    CONSTRAINT user_profiles_user_id_key UNIQUE (user_id),
    CONSTRAINT user_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users (id) ON DELETE CASCADE,
    CONSTRAINT user_profiles_age_check CHECK (
        (age >= 1) AND (age <= 120)
    )
) TABLESPACE pg_default;

-- Create indexes for user_profiles
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON public.user_profiles USING btree (user_id) TABLESPACE pg_default;
CREATE INDEX IF NOT EXISTS idx_user_profiles_email ON public.user_profiles USING btree (email) TABLESPACE pg_default;
CREATE INDEX IF NOT EXISTS idx_user_profiles_created_at ON public.user_profiles USING btree (created_at) TABLESPACE pg_default;

-- Create triggers for user_profiles
CREATE TRIGGER set_user_profiles_email
    BEFORE INSERT OR UPDATE ON user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION set_user_email();

CREATE TRIGGER update_user_profiles_updated_at
    BEFORE UPDATE ON user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ===========================================
-- ADMIN USERS TABLE
-- ===========================================

-- Drop table if exists (for clean setup)
DROP TABLE IF EXISTS public.admin_users CASCADE;

-- Create admin_users table
CREATE TABLE public.admin_users (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id uuid NULL,
    is_admin boolean NULL DEFAULT false,
    created_at timestamp with time zone NULL DEFAULT now(),
    updated_at timestamp with time zone NULL DEFAULT now(),
    CONSTRAINT admin_users_pkey PRIMARY KEY (id),
    CONSTRAINT admin_users_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users (id) ON DELETE CASCADE
) TABLESPACE pg_default;

-- Create indexes for admin_users
CREATE INDEX IF NOT EXISTS idx_admin_users_user_id ON public.admin_users USING btree (user_id) TABLESPACE pg_default;
CREATE INDEX IF NOT EXISTS idx_admin_users_is_admin ON public.admin_users USING btree (is_admin) TABLESPACE pg_default;
CREATE UNIQUE INDEX IF NOT EXISTS uq_admin_users_user_id ON public.admin_users USING btree (user_id) TABLESPACE pg_default;

-- Create trigger for admin_users
CREATE TRIGGER update_admin_users_updated_at
    BEFORE UPDATE ON admin_users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ===========================================
-- AUTH USERS TRIGGER
-- ===========================================

-- Create trigger on auth.users to automatically create profile and admin records
CREATE OR REPLACE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION handle_new_user();

-- ===========================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ===========================================

-- Enable RLS on both tables
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.admin_users ENABLE ROW LEVEL SECURITY;

-- User profiles policies
-- Users can view their own profile
CREATE POLICY "Users can view own profile" ON public.user_profiles
    FOR SELECT USING (auth.uid() = user_id);

-- Users can update their own profile
CREATE POLICY "Users can update own profile" ON public.user_profiles
    FOR UPDATE USING (auth.uid() = user_id);

-- Users can insert their own profile
CREATE POLICY "Users can insert own profile" ON public.user_profiles
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Admins can view all profiles
CREATE POLICY "Admins can view all profiles" ON public.user_profiles
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.admin_users 
            WHERE user_id = auth.uid() AND is_admin = true
        )
    );

-- Admins can update all profiles
CREATE POLICY "Admins can update all profiles" ON public.user_profiles
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM public.admin_users 
            WHERE user_id = auth.uid() AND is_admin = true
        )
    );

-- Admin users policies
-- Users can view their own admin status
CREATE POLICY "Users can view own admin status" ON public.admin_users
    FOR SELECT USING (auth.uid() = user_id);

-- Admins can view all admin statuses
CREATE POLICY "Admins can view all admin statuses" ON public.admin_users
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.admin_users 
            WHERE user_id = auth.uid() AND is_admin = true
        )
    );

-- Admins can update admin statuses
CREATE POLICY "Admins can update admin statuses" ON public.admin_users
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM public.admin_users 
            WHERE user_id = auth.uid() AND is_admin = true
        )
    );

-- Admins can insert admin statuses
CREATE POLICY "Admins can insert admin statuses" ON public.admin_users
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.admin_users 
            WHERE user_id = auth.uid() AND is_admin = true
        )
    );

-- ===========================================
-- GRANT PERMISSIONS
-- ===========================================

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON public.user_profiles TO anon, authenticated;
GRANT ALL ON public.admin_users TO anon, authenticated;
GRANT USAGE ON SCHEMA auth TO anon, authenticated;

-- ===========================================
-- VERIFICATION QUERIES
-- ===========================================

-- Check if tables exist
SELECT 
    schemaname,
    tablename,
    tableowner
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename IN ('user_profiles', 'admin_users')
ORDER BY tablename;

-- Check if functions exist
SELECT 
    routine_name,
    routine_type
FROM information_schema.routines 
WHERE routine_schema = 'public' 
AND routine_name IN ('update_updated_at_column', 'set_user_email', 'handle_new_user')
ORDER BY routine_name;

-- Check if triggers exist
SELECT 
    trigger_name,
    event_object_table,
    action_timing,
    event_manipulation
FROM information_schema.triggers 
WHERE trigger_schema = 'public'
ORDER BY event_object_table, trigger_name;
