-- ===========================================
-- STEP 1: CREATE REQUIRED FUNCTIONS
-- ===========================================

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

-- Function to handle new user signup
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
-- STEP 2: CREATE USER_PROFILES TABLE
-- ===========================================

CREATE TABLE IF NOT EXISTS public.user_profiles (
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
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON public.user_profiles (user_id);
CREATE INDEX IF NOT EXISTS idx_user_profiles_email ON public.user_profiles (email);
CREATE INDEX IF NOT EXISTS idx_user_profiles_created_at ON public.user_profiles (created_at);

-- ===========================================
-- STEP 3: CREATE ADMIN_USERS TABLE
-- ===========================================

CREATE TABLE IF NOT EXISTS public.admin_users (
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    user_id uuid NULL,
    is_admin boolean NULL DEFAULT false,
    created_at timestamp with time zone NULL DEFAULT now(),
    updated_at timestamp with time zone NULL DEFAULT now(),
    CONSTRAINT admin_users_pkey PRIMARY KEY (id),
    CONSTRAINT admin_users_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users (id) ON DELETE CASCADE
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_admin_users_user_id ON public.admin_users (user_id);
CREATE INDEX IF NOT EXISTS idx_admin_users_is_admin ON public.admin_users (is_admin);
CREATE UNIQUE INDEX IF NOT EXISTS uq_admin_users_user_id ON public.admin_users (user_id);

-- ===========================================
-- STEP 4: CREATE TRIGGERS
-- ===========================================

-- User profiles triggers
DROP TRIGGER IF EXISTS set_user_profiles_email ON public.user_profiles;
CREATE TRIGGER set_user_profiles_email
    BEFORE INSERT OR UPDATE ON public.user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION set_user_email();

DROP TRIGGER IF EXISTS update_user_profiles_updated_at ON public.user_profiles;
CREATE TRIGGER update_user_profiles_updated_at
    BEFORE UPDATE ON public.user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Admin users triggers
DROP TRIGGER IF EXISTS update_admin_users_updated_at ON public.admin_users;
CREATE TRIGGER update_admin_users_updated_at
    BEFORE UPDATE ON public.admin_users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Auth users trigger
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION handle_new_user();

-- ===========================================
-- STEP 5: ENABLE ROW LEVEL SECURITY
-- ===========================================

ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.admin_users ENABLE ROW LEVEL SECURITY;

-- ===========================================
-- STEP 6: CREATE RLS POLICIES
-- ===========================================

-- User profiles policies
DROP POLICY IF EXISTS "Users can view own profile" ON public.user_profiles;
CREATE POLICY "Users can view own profile" ON public.user_profiles
    FOR SELECT USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can update own profile" ON public.user_profiles;
CREATE POLICY "Users can update own profile" ON public.user_profiles
    FOR UPDATE USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Users can insert own profile" ON public.user_profiles;
CREATE POLICY "Users can insert own profile" ON public.user_profiles
    FOR INSERT WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Admins can view all profiles" ON public.user_profiles;
CREATE POLICY "Admins can view all profiles" ON public.user_profiles
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.admin_users 
            WHERE user_id = auth.uid() AND is_admin = true
        )
    );

-- Admin users policies
DROP POLICY IF EXISTS "Users can view own admin status" ON public.admin_users;
CREATE POLICY "Users can view own admin status" ON public.admin_users
    FOR SELECT USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Admins can view all admin statuses" ON public.admin_users;
CREATE POLICY "Admins can view all admin statuses" ON public.admin_users
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.admin_users 
            WHERE user_id = auth.uid() AND is_admin = true
        )
    );

-- ===========================================
-- STEP 7: GRANT PERMISSIONS
-- ===========================================

GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON public.user_profiles TO anon, authenticated;
GRANT ALL ON public.admin_users TO anon, authenticated;
