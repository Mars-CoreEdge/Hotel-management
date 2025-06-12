#!/usr/bin/env python3
"""
Script to reset the hotel database with new schema
"""
import os
import sys

def reset_database():
    """Delete old database and let the system create a fresh one"""
    
    print("🔄 Resetting Hotel Management Database...")
    
    # Database file path
    db_file = "hotel.db"
    
    # Try to remove the old database file
    try:
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"✅ Removed old database file: {db_file}")
        else:
            print(f"ℹ️  No existing database file found: {db_file}")
    except Exception as e:
        print(f"⚠️  Could not remove database file: {e}")
    
    # Now try to create the new database
    try:
        print("🔧 Creating new database with updated schema...")
        
        # Import and create database
        import database
        database.create_database()
        
        print("🎉 Database reset completed successfully!")
        print("📊 New schema includes: Rooms, Guests, and Bookings tables")
        print("🚀 You can now start the FastAPI server: python main.py")
        
    except Exception as e:
        print(f"❌ Error creating new database: {e}")
        print("🔧 Make sure all Python dependencies are installed")
        return False
    
    return True

if __name__ == "__main__":
    print("🏨 Hotel Management Database Reset Tool")
    print("=" * 50)
    
    success = reset_database()
    
    if success:
        print("\n✅ Database reset successful!")
        print("🚀 Ready to start the FastAPI server!")
    else:
        print("\n❌ Database reset failed!")
        print("🔧 Please check the error messages above.")
        sys.exit(1) 