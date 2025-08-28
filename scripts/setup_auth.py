#!/usr/bin/env python3
"""
Authentication System Setup Script
This script helps set up the authentication system for the Grand Hotel Management System.
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file with required environment variables"""
    env_content = """# Supabase Configuration
SUPABASE_URL=your-supabase-project-url
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Existing Configuration
HOST=0.0.0.0
PORT=8001
DATABASE_URL=sqlite:///hotel.db
DEBUG=False
RELOAD=False

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=500
OPENAI_TEMPERATURE=0.7

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=grandhotel@gmail.com
EMAIL_PASSWORD=demo-password-12345
USE_TLS=True
EMAIL_DEMO_MODE=True

# Hotel Information
HOTEL_NAME=Grand Hotel
HOTEL_ADDRESS=123 Luxury Avenue, Hotel District, City 12345
HOTEL_PHONE=+1-555-HOTEL-1
HOTEL_WEBSITE=https://grandhotel.com

# Admin Configuration
ADMIN_EMAIL=grandhotel@gmail.com
ENABLE_ADMIN_NOTIFICATIONS=True
"""
    
    env_path = Path('.env')
    if env_path.exists():
        print("⚠️  .env file already exists. Backing up to .env.backup")
        os.rename('.env', '.env.backup')
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file")
    return True

def create_react_env_file():
    """Create React .env file"""
    react_env_content = """# Supabase Configuration
REACT_APP_SUPABASE_URL=your-supabase-project-url
REACT_APP_SUPABASE_ANON_KEY=your-supabase-anon-key

# Backend API Configuration
REACT_APP_API_URL=http://localhost:8001
"""
    
    react_env_path = Path('fruit-store-ui/.env')
    if react_env_path.exists():
        print("⚠️  React .env file already exists. Backing up to .env.backup")
        os.rename(react_env_path, react_env_path.with_suffix('.env.backup'))
    
    react_env_path.parent.mkdir(exist_ok=True)
    with open(react_env_path, 'w') as f:
        f.write(react_env_content)
    
    print("✅ Created React .env file")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    try:
        import fastapi
        import supabase
        import jose
        import passlib
        print("✅ Python dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False
    
    # Check if React dependencies exist
    package_json = Path('fruit-store-ui/package.json')
    if not package_json.exists():
        print("❌ React app not found. Make sure you're in the project root directory.")
        return False
    
    print("✅ React app found")
    return True

def print_setup_instructions():
    """Print setup instructions"""
    print("\n" + "="*60)
    print("🔐 AUTHENTICATION SYSTEM SETUP INSTRUCTIONS")
    print("="*60)
    
    print("\n1️⃣  SUPABASE PROJECT SETUP:")
    print("   • Go to https://supabase.com and create a new project")
    print("   • Get your Project URL and API keys from Settings > API")
    print("   • Enable Email Authentication in Authentication > Settings")
    
    print("\n2️⃣  UPDATE ENVIRONMENT VARIABLES:")
    print("   • Edit .env file in the root directory")
    print("   • Edit fruit-store-ui/.env file")
    print("   • Replace placeholder values with your actual Supabase credentials")
    
    print("\n3️⃣  INSTALL FRONTEND DEPENDENCIES:")
    print("   • cd fruit-store-ui")
    print("   • npm install")
    
    print("\n4️⃣  START THE SYSTEM:")
    print("   • Backend: python app/main.py")
    print("   • Frontend: cd fruit-store-ui && npm start")
    
    print("\n5️⃣  TEST THE SYSTEM:")
    print("   • Visit http://localhost:3000")
    print("   • Create an admin account at /signup")
    print("   • Test login and role-based access")
    
    print("\n📚 For detailed instructions, see docs/AUTHENTICATION_SETUP.md")
    print("="*60)

def main():
    """Main setup function"""
    print("🚀 Setting up Authentication System for Grand Hotel Management System")
    print("="*60)
    
    # Check if we're in the right directory
    if not Path('app').exists() or not Path('fruit-store-ui').exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create environment files
    try:
        create_env_file()
        create_react_env_file()
    except Exception as e:
        print(f"❌ Error creating environment files: {e}")
        sys.exit(1)
    
    # Print setup instructions
    print_setup_instructions()
    
    print("\n🎉 Setup complete! Follow the instructions above to configure your system.")

if __name__ == "__main__":
    main()
