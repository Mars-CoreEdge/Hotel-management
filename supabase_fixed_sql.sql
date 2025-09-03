-- =====================================================
-- SUPABASE USER PROFILES TABLE SETUP (FIXED VERSION)
-- =====================================================

-- 1. Drop existing table if it exists (for clean setup)
DROP TABLE IF EXISTS user_profiles CASCADE;

-- 2. Create the user_profiles table with proper constraints
CREATE TABLE user_profiles (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL UNIQUE,
  email TEXT NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  phone TEXT,
  country TEXT,
  age INTEGER CHECK (age >= 1 AND age <= 120),
  profile_picture_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_user_profiles_email ON user_profiles(email);
CREATE INDEX IF NOT EXISTS idx_user_profiles_created_at ON user_profiles(created_at);

-- 4. Enable Row Level Security (RLS)
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- 5. Create RLS policies for data security
-- Policy: Users can view their own profile
CREATE POLICY "Users can view own profile" ON user_profiles
  FOR SELECT USING (auth.uid() = user_id);

-- Policy: Users can insert their own profile
CREATE POLICY "Users can insert own profile" ON user_profiles
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Policy: Users can update their own profile
CREATE POLICY "Users can update own profile" ON user_profiles
  FOR UPDATE USING (auth.uid() = user_id);

-- Policy: Users can delete their own profile
CREATE POLICY "Users can delete own profile" ON user_profiles
  FOR DELETE USING (auth.uid() = user_id);

-- 6. Create a function to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 7. Create trigger to automatically update updated_at
CREATE TRIGGER update_user_profiles_updated_at
    BEFORE UPDATE ON user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 8. Create a function to automatically set email from auth.users
CREATE OR REPLACE FUNCTION set_user_email()
RETURNS TRIGGER AS $$
BEGIN
    -- If email is not provided, get it from auth.users
    IF NEW.email IS NULL OR NEW.email = '' THEN
        SELECT email INTO NEW.email
        FROM auth.users
        WHERE id = NEW.user_id;
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 9. Create trigger to automatically set email
CREATE TRIGGER set_user_profiles_email
    BEFORE INSERT OR UPDATE ON user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION set_user_email();

-- 10. Create a function to upsert user profile (FIXED VERSION)
CREATE OR REPLACE FUNCTION upsert_user_profile(
  p_first_name TEXT,
  p_last_name TEXT,
  p_email TEXT DEFAULT NULL,
  p_phone TEXT DEFAULT NULL,
  p_country TEXT DEFAULT NULL,
  p_age INTEGER DEFAULT NULL,
  p_profile_picture_url TEXT DEFAULT NULL
)
RETURNS user_profiles
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  result user_profiles;
  current_user_id UUID;
BEGIN
  -- Get current user ID
  current_user_id := auth.uid();

  -- Check if user is authenticated
  IF current_user_id IS NULL THEN
    RAISE EXCEPTION 'User not authenticated';
  END IF;

  -- If email is not provided, get it from auth.users
  IF p_email IS NULL OR p_email = '' THEN
    SELECT email INTO p_email
    FROM auth.users
    WHERE id = current_user_id;
  END IF;

  -- Insert or update profile using user_id as the unique constraint
  INSERT INTO user_profiles (
    user_id, email, first_name, last_name,
    phone, country, age, profile_picture_url
  ) VALUES (
    current_user_id, p_email, p_first_name, p_last_name,
    p_phone, p_country, p_age, p_profile_picture_url
  )
  ON CONFLICT (user_id)  -- This now works because user_id has UNIQUE constraint
  DO UPDATE SET
    first_name = EXCLUDED.first_name,
    last_name = EXCLUDED.last_name,
    email = EXCLUDED.email,
    phone = EXCLUDED.phone,
    country = EXCLUDED.country,
    age = EXCLUDED.age,
    profile_picture_url = EXCLUDED.profile_picture_url,
    updated_at = NOW()
  RETURNING * INTO result;

  RETURN result;
END;
$$;

-- 11. Create a function to get user profile
CREATE OR REPLACE FUNCTION get_user_profile()
RETURNS user_profiles
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  result user_profiles;
  current_user_id UUID;
BEGIN
  -- Get current user ID
  current_user_id := auth.uid();

  -- Check if user is authenticated
  IF current_user_id IS NULL THEN
    RAISE EXCEPTION 'User not authenticated';
  END IF;

  -- Get user profile
  SELECT * INTO result
  FROM user_profiles
  WHERE user_id = current_user_id;

  RETURN result;
END;
$$;

-- 12. Create a function to delete user profile
CREATE OR REPLACE FUNCTION delete_user_profile()
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  current_user_id UUID;
  deleted_count INTEGER;
BEGIN
  -- Get current user ID
  current_user_id := auth.uid();

  -- Check if user is authenticated
  IF current_user_id IS NULL THEN
    RAISE EXCEPTION 'User not authenticated';
  END IF;

  -- Delete user profile
  DELETE FROM user_profiles
  WHERE user_id = current_user_id;

  GET DIAGNOSTICS deleted_count = ROW_COUNT;

  RETURN deleted_count > 0;
END;
$$;

-- 13. Grant necessary permissions
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT ALL ON user_profiles TO authenticated;
GRANT EXECUTE ON FUNCTION upsert_user_profile TO authenticated;
GRANT EXECUTE ON FUNCTION get_user_profile TO authenticated;
GRANT EXECUTE ON FUNCTION delete_user_profile TO authenticated;

-- 14. Add comments for documentation
COMMENT ON TABLE user_profiles IS 'User profile information linked to Supabase auth users';
COMMENT ON COLUMN user_profiles.user_id IS 'References auth.users(id) - the authenticated user (UNIQUE)';
COMMENT ON COLUMN user_profiles.email IS 'User email - automatically synced from auth.users if not provided';
COMMENT ON COLUMN user_profiles.age IS 'User age with validation (1-120)';
COMMENT ON FUNCTION upsert_user_profile IS 'Create or update user profile - automatically uses authenticated user ID';
COMMENT ON FUNCTION get_user_profile IS 'Get current user profile - automatically uses authenticated user ID';
COMMENT ON FUNCTION delete_user_profile IS 'Delete current user profile - automatically uses authenticated user ID';
