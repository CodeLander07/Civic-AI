#!/usr/bin/env python3
"""
Verification script to ensure all dependencies are installed correctly
"""

import sys
import os
from dotenv import load_dotenv

def check_imports():
    """Check if all required imports work"""
    print("🔍 Checking imports...")
    
    try:
        from supabase import create_client, Client
        print("✅ Supabase import successful")
    except ImportError as e:
        print(f"❌ Supabase import failed: {e}")
        return False
    
    try:
        from fastapi import FastAPI, HTTPException, Depends, status
        from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
        print("✅ FastAPI imports successful")
    except ImportError as e:
        print(f"❌ FastAPI imports failed: {e}")
        return False
    
    try:
        from pydantic import BaseModel, EmailStr
        print("✅ Pydantic imports successful")
    except ImportError as e:
        print(f"❌ Pydantic imports failed: {e}")
        return False
    
    return True

def check_environment():
    """Check environment variables"""
    print("\n🔍 Checking environment variables...")
    
    load_dotenv()
    
    required_vars = ["SUPABASE_URL", "SUPABASE_ANON_KEY"]
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        elif value == "your_supabase_anon_key_here":
            print(f"⚠️  {var} is set to placeholder value")
        else:
            print(f"✅ {var} is configured")
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    return True

def test_supabase_connection():
    """Test Supabase client initialization"""
    print("\n🔍 Testing Supabase connection...")
    
    try:
        load_dotenv()
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_anon_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_anon_key:
            print("❌ Missing Supabase credentials")
            return False
        
        from supabase import create_client
        supabase = create_client(supabase_url, supabase_anon_key)
        print("✅ Supabase client initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False

def test_app_import():
    """Test FastAPI app import"""
    print("\n🔍 Testing FastAPI app import...")
    
    try:
        import main
        print("✅ FastAPI app imported successfully")
        return True
    except Exception as e:
        print(f"❌ FastAPI app import failed: {e}")
        return False

def main():
    print("🚀 Verifying Civic-AI Backend Setup")
    print("=" * 50)
    
    success = True
    
    # Check imports
    if not check_imports():
        success = False
    
    # Check environment
    if not check_environment():
        success = False
    
    # Test Supabase connection
    if not test_supabase_connection():
        success = False
    
    # Test app import
    if not test_app_import():
        success = False
    
    print("\n" + "=" * 50)
    
    if success:
        print("🎉 All checks passed! Backend is ready to run.")
        print("\n📋 To start the server:")
        print("uvicorn main:app --reload")
        print("\n📋 Available endpoints:")
        print("- GET  /              - Health check")
        print("- GET  /health        - Detailed health status")
        print("- POST /auth/signup   - User registration")
        print("- POST /auth/login    - User authentication")
        print("- GET  /auth/me       - Get current user (protected)")
        print("- POST /api/query     - AI query processing (protected)")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()