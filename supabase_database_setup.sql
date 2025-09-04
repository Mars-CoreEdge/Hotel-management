-- =====================================================
-- DATABASE SETUP FOR SUPABASE PROJECT: rmweyfpxxnonlojspbkn
-- =====================================================

-- 1. Create admin_users table for admin management
CREATE TABLE IF NOT EXISTS admin_users (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL UNIQUE,
  is_admin BOOLEAN DEFAULT FALSE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Create user_profiles table
CREATE TABLE IF NOT EXISTS user_profiles (
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
CREATE INDEX IF NOT EXISTS idx_admin_users_user_id ON admin_users(user_id);
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_user_profiles_email ON user_profiles(email);

-- 4. Enable Row Level Security (RLS)
ALTER TABLE admin_users ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- 5. Create RLS policies for admin_users
CREATE POLICY "Users can view own admin status" ON admin_users
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Admins can view all admin statuses" ON admin_users
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM admin_users 
      WHERE user_id = auth.uid() AND is_admin = true
    )
  );

CREATE POLICY "System can insert admin records" ON admin_users
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Admins can update admin status" ON admin_users
  FOR UPDATE USING (
    EXISTS (
      SELECT 1 FROM admin_users 
      WHERE user_id = auth.uid() AND is_admin = true
    )
  );

-- 6. Create RLS policies for user_profiles
CREATE POLICY "Users can view own profile" ON user_profiles
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own profile" ON user_profiles
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own profile" ON user_profiles
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own profile" ON user_profiles
  FOR DELETE USING (auth.uid() = user_id);

-- 7. Create function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 8. Create triggers for updated_at
CREATE TRIGGER update_admin_users_updated_at
    BEFORE UPDATE ON admin_users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at
    BEFORE UPDATE ON user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 9. Create function to automatically set email from auth.users
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

-- 10. Create trigger to automatically set email
CREATE TRIGGER set_user_profiles_email
    BEFORE INSERT OR UPDATE ON user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION set_user_email();

-- 11. Create function to handle new user signup
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  -- Insert into admin_users table (default: not admin)
  INSERT INTO admin_users (user_id, is_admin)
  VALUES (NEW.id, false);
  
  -- Insert into user_profiles table with data from user_metadata
  INSERT INTO user_profiles (user_id, email, first_name, last_name, phone)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'firstName', ''),
    COALESCE(NEW.raw_user_meta_data->>'lastName', ''),
    COALESCE(NEW.raw_user_meta_data->>'phone', '')
  );
  
  RETURN NEW;
END;
$$ language 'plpgsql' SECURITY DEFINER;

-- 12. Create trigger to handle new user signup
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- 13. Create function to upsert user profile
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

-- 14. Create function to get user profile
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

-- 15. Create function to check admin status
CREATE OR REPLACE FUNCTION is_admin(user_id UUID DEFAULT auth.uid())
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  admin_status BOOLEAN;
BEGIN
  -- Check if user is admin
  SELECT is_admin INTO admin_status
  FROM admin_users
  WHERE admin_users.user_id = is_admin.user_id;
  
  RETURN COALESCE(admin_status, false);
END;
$$;

-- 16. Grant necessary permissions
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT ALL ON admin_users TO authenticated;
GRANT ALL ON user_profiles TO authenticated;
GRANT EXECUTE ON FUNCTION upsert_user_profile TO authenticated;
GRANT EXECUTE ON FUNCTION get_user_profile TO authenticated;
GRANT EXECUTE ON FUNCTION is_admin TO authenticated;

-- 17. Add comments for documentation
COMMENT ON TABLE admin_users IS 'Admin user management table';
COMMENT ON TABLE user_profiles IS 'User profile information linked to Supabase auth users';
COMMENT ON FUNCTION handle_new_user IS 'Automatically creates admin and profile records for new users';
COMMENT ON FUNCTION upsert_user_profile IS 'Create or update user profile';
COMMENT ON FUNCTION get_user_profile IS 'Get current user profile';
COMMENT ON FUNCTION is_admin IS 'Check if user is admin';
