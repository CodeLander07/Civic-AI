#!/usr/bin/env python3
"""
Installation script for Civic-AI authentication setup
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False
    return True

def check_env_variables():
    """Check if required environment variables are set"""
    print("Checking environment variables...")
    
    required_vars = ["SUPABASE_URL", "SUPABASE_ANON_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please update your .env file with the correct Supabase credentials")
        return False
    
    print("✅ Environment variables are set")
    return True

def main():
    print("🚀 Setting up Civic-AI Authentication...")
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Check environment variables
    if not check_env_variables():
        print("\n📝 Please update your .env file with:")
        print("SUPABASE_URL=your_supabase_url")
        print("SUPABASE_ANON_KEY=your_supabase_anon_key")
        sys.exit(1)
    
    print("\n✅ Authentication setup complete!")
    print("\n📋 Next steps:")
    print("1. Create the 'users' table in your Supabase database using the SQL in main.py")
    print("2. Run: uvicorn main:app --reload")
    print("3. Test the endpoints:")
    print("   - POST /auth/signup")
    print("   - POST /auth/login") 
    print("   - GET /auth/me")

if __name__ == "__main__":
    main()