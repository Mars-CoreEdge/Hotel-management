#!/usr/bin/env python3
"""
Script to set up the first admin user in Supabase
Run this after creating the admin_users table
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_first_admin():
    """Set up the first admin user"""
    print("🔧 Setting up first admin user in Supabase")
    print("=" * 50)
    
    # Check if Supabase credentials are configured
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    
    if not supabase_url or not supabase_service_key:
        print("❌ Error: Supabase credentials not found in .env file")
        print("Please make sure you have:")
        print("  - SUPABASE_URL")
        print("  - SUPABASE_SERVICE_ROLE_KEY")
        return False
    
    print("✅ Supabase credentials found")
    print(f"📡 URL: {supabase_url}")
    
    # Instructions for manual setup
    print("\n📋 Manual Setup Instructions:")
    print("1. Go to your Supabase Dashboard")
    print("2. Navigate to SQL Editor")
    print("3. Run the following SQL commands:")
    
    print("\n🔑 Create admin_users table:")
    print("""
-- Create admin table to store admin status
CREATE TABLE IF NOT EXISTS admin_users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_admin_users_user_id ON admin_users(user_id);
CREATE INDEX IF NOT EXISTS idx_admin_users_is_admin ON admin_users(is_admin);

-- Enable Row Level Security
ALTER TABLE admin_users ENABLE ROW LEVEL SECURITY;

-- RLS Policies
-- Users can only see their own admin status
CREATE POLICY "Users can view own admin status" ON admin_users
    FOR SELECT USING (auth.uid() = user_id);

-- Only super admins can insert/update admin status
CREATE POLICY "Super admins can manage admin status" ON admin_users
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM admin_users 
            WHERE user_id = auth.uid() AND is_admin = TRUE
        )
    );

-- Function to automatically create admin record for new users
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO admin_users (user_id, is_admin)
    VALUES (NEW.id, FALSE);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to automatically create admin record
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- Function to check if user is admin
CREATE OR REPLACE FUNCTION is_user_admin(user_uuid UUID)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM admin_users 
        WHERE user_id = user_uuid AND is_admin = TRUE
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
""")
    
    print("\n👑 Make first user admin:")
    print("""
-- After creating a user account, make them admin
-- Replace 'USER_EMAIL_HERE' with the actual email
UPDATE admin_users 
SET is_admin = TRUE 
WHERE user_id = (
    SELECT id FROM auth.users 
    WHERE email = 'USER_EMAIL_HERE'
);
""")
    
    print("\n📝 Alternative: Make user admin by ID:")
    print("""
-- Or make admin by user ID (found in auth.users table)
UPDATE admin_users 
SET is_admin = TRUE 
WHERE user_id = 'USER_UUID_HERE';
""")
    
    print("\n🔍 Check admin status:")
    print("""
-- Verify admin status
SELECT 
    au.email,
    adu.is_admin,
    adu.created_at
FROM auth.users au
JOIN admin_users adu ON au.id = adu.user_id
WHERE au.email = 'USER_EMAIL_HERE';
""")
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Run the SQL commands in Supabase Dashboard")
    print("2. Create a user account through your app")
    print("3. Make that user admin using the UPDATE command")
    print("4. Test admin access in your React app")
    
    return True

if __name__ == "__main__":
    try:
        setup_first_admin()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
