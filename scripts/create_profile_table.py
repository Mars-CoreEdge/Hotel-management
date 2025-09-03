#!/usr/bin/env python3
"""
Script to create the user_profiles table in the database
"""

import sqlite3
import os
from datetime import datetime

def create_profile_table():
    """Create the user_profiles table"""
    
    # Get the database path
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'hotel.db')
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create the user_profiles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                country TEXT,
                age INTEGER,
                profile_picture_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create an index on user_id for faster lookups
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id 
            ON user_profiles(user_id)
        ''')
        
        # Create an index on email for faster lookups
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_user_profiles_email 
            ON user_profiles(email)
        ''')
        
        # Commit the changes
        conn.commit()
        
        print("✅ User profiles table created successfully!")
        print(f"📊 Database: {db_path}")
        print("🔍 Created indexes on user_id and email for better performance")
        
        # Show table structure
        cursor.execute("PRAGMA table_info(user_profiles)")
        columns = cursor.fetchall()
        
        print("\n📋 Table structure:")
        print("Column Name | Type | Not Null | Default")
        print("-" * 50)
        for col in columns:
            print(f"{col[1]:<12} | {col[2]:<8} | {col[3]:<8} | {col[4] or 'None'}")
        
    except sqlite3.Error as e:
        print(f"❌ Error creating table: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        if conn:
            conn.close()
    
    return True

if __name__ == "__main__":
    print("🚀 Creating user profiles table...")
    print("=" * 50)
    
    success = create_profile_table()
    
    if success:
        print("\n🎉 Profile system setup complete!")
        print("💡 You can now use the profile functionality in your application.")
    else:
        print("\n💥 Setup failed. Please check the error messages above.")
