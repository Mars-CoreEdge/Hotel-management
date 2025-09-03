-- =====================================================
-- SIMPLE SUPABASE USER PROFILES SETUP
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

-- 4. Enable Row Level Security (RLS)
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- 5. Create RLS policies for data security
CREATE POLICY "Users can view own profile" ON user_profiles
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own profile" ON user_profiles
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own profile" ON user_profiles
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own profile" ON user_profiles
  FOR DELETE USING (auth.uid() = user_id);

-- 6. Create a simple upsert function
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

  -- Insert or update profile
  INSERT INTO user_profiles (
    user_id, email, first_name, last_name,
    phone, country, age, profile_picture_url
  ) VALUES (
    current_user_id, p_email, p_first_name, p_last_name,
    p_phone, p_country, p_age, p_profile_picture_url
  )
  ON CONFLICT (user_id)
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

-- 7. Create a simple get function
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

-- 8. Create a simple delete function
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

-- 9. Grant necessary permissions
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT ALL ON user_profiles TO authenticated;
GRANT EXECUTE ON FUNCTION upsert_user_profile TO authenticated;
GRANT EXECUTE ON FUNCTION get_user_profile TO authenticated;
GRANT EXECUTE ON FUNCTION delete_user_profile TO authenticated;
