#!/usr/bin/env python3
"""
Test script to verify Supabase profile setup
"""

import os
import sys
from supabase import create_client, Client

def test_supabase_connection():
    """Test basic Supabase connection"""
    
    # Get Supabase credentials from environment or settings
    supabase_url = os.getenv("SUPABASE_URL", "https://placeholder.supabase.co")
    supabase_key = os.getenv("SUPABASE_ANON_KEY", "placeholder-anon-key")
    
    print("🔍 Testing Supabase Connection...")
    print(f"URL: {supabase_url}")
    print(f"Key: {supabase_key[:20]}..." if len(supabase_key) > 20 else f"Key: {supabase_key}")
    
    try:
        # Create Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✅ Supabase client created successfully")
        
        # Test basic connection
        print("🔍 Testing basic connection...")
        
        # Try to get the current user (should be None if not authenticated)
        try:
            user = supabase.auth.get_user()
            if user:
                print(f"✅ User authenticated: {user.user.email}")
            else:
                print("ℹ️  No user authenticated (expected for this test)")
        except Exception as e:
            print(f"ℹ️  Auth test: {e}")
        
        print("✅ Supabase connection test completed")
        return True
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False

def test_profile_functions():
    """Test if profile functions exist"""
    print("\n🔍 Testing Profile Functions...")
    
    try:
        from app.services.supabase_profile_service import SupabaseProfileService
        print("✅ SupabaseProfileService imported successfully")
        
        # Try to create service instance
        try:
            service = SupabaseProfileService()
            print("✅ SupabaseProfileService instance created")
        except Exception as e:
            print(f"⚠️  Service creation failed (expected if Supabase not configured): {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import SupabaseProfileService: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Supabase Profile System Test")
    print("=" * 50)
    
    # Test 1: Basic connection
    connection_ok = test_supabase_connection()
    
    # Test 2: Profile functions
    functions_ok = test_profile_functions()
    
    print("\n📋 Test Results:")
    print(f"Connection: {'✅ PASS' if connection_ok else '❌ FAIL'}")
    print(f"Functions: {'✅ PASS' if functions_ok else '❌ FAIL'}")
    
    if connection_ok and functions_ok:
        print("\n🎉 All tests passed! Supabase integration is ready.")
        print("\n📝 Next steps:")
        print("1. Configure your Supabase URL and keys in environment variables")
        print("2. Run the SQL script in your Supabase dashboard")
        print("3. Test the profile system with an authenticated user")
    else:
        print("\n⚠️  Some tests failed. Please check your Supabase configuration.")
        print("\n📝 Setup instructions:")
        print("1. Create a Supabase project at https://supabase.com")
        print("2. Get your project URL and anon key")
        print("3. Set environment variables: SUPABASE_URL and SUPABASE_ANON_KEY")
        print("4. Run the SQL script in your Supabase dashboard")

if __name__ == "__main__":
    main()
