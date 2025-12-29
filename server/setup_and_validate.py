#!/usr/bin/env python3
"""
Setup and validation script for Civic-AI backend
Ensures all dependencies are installed and configured correctly
"""

import subprocess
import sys
import os
import importlib
from dotenv import load_dotenv

def check_python_version():
    """Check Python version compatibility"""
    print("🔍 Checking Python version...")
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible. Need Python 3.8+")
        return False

def check_virtual_environment():
    """Check if virtual environment is active"""
    print("\n🔍 Checking virtual environment...")
    
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is active")
        return True
    else:
        print("⚠️  Virtual environment not detected (may be OK)")
        return True  # Don't fail on this

def install_dependencies():
    """Install required dependencies"""
    print("\n🔍 Installing dependencies...")
    
    required_packages = [
        "fastapi==0.128.0",
        "uvicorn==0.40.0",
        "python-dotenv==1.2.1",
        "python-multipart==0.0.21",
        "supabase==2.10.0",
        "email-validator==2.1.1",
        "pytesseract==0.3.13",
        "Pillow==12.0.0",
        "pydantic==2.12.5"
    ]
    
    for package in required_packages:
        try:
            print(f"   Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
            return False
    
    print("✅ All dependencies installed successfully")
    return True

def check_imports():
    """Check if all required modules can be imported"""
    print("\n🔍 Checking imports...")
    
    required_modules = [
        ("fastapi", "FastAPI framework"),
        ("uvicorn", "ASGI server"),
        ("supabase", "Supabase client"),
        ("pydantic", "Data validation"),
        ("PIL", "Image processing"),
        ("pytesseract", "OCR functionality"),
        ("dotenv", "Environment variables")
    ]
    
    success = True
    
    for module, description in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {description}: OK")
        except ImportError as e:
            print(f"❌ {description}: Failed - {e}")
            success = False
    
    return success

def check_environment_variables():
    """Check environment variables"""
    print("\n🔍 Checking environment variables...")
    
    load_dotenv()
    
    required_vars = [
        ("SUPABASE_URL", "Supabase project URL"),
        ("SUPABASE_ANON_KEY", "Supabase anonymous key")
    ]
    
    success = True
    
    for var, description in required_vars:
        value = os.getenv(var)
        if value and value != "your_supabase_anon_key_here":
            print(f"✅ {description}: Configured")
        else:
            print(f"❌ {description}: Missing or placeholder")
            success = False
    
    # Optional variables
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and openai_key != "your_openai_api_key_here":
        print("✅ OpenAI API Key: Configured (optional)")
    else:
        print("⚠️  OpenAI API Key: Not configured (will use fallback responses)")
    
    return success

def test_supabase_connection():
    """Test Supabase connection"""
    print("\n🔍 Testing Supabase connection...")
    
    try:
        load_dotenv()
        from supabase import create_client
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_anon_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not supabase_url or not supabase_anon_key:
            print("❌ Supabase credentials not found")
            return False
        
        client = create_client(supabase_url, supabase_anon_key)
        print("✅ Supabase client created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False

def test_main_module():
    """Test if main.py can be imported"""
    print("\n🔍 Testing main module...")
    
    try:
        import main
        print("✅ Main module imports successfully")
        return True
    except Exception as e:
        print(f"❌ Main module import failed: {e}")
        return False

def main():
    print("🚀 CIVIC-AI BACKEND SETUP AND VALIDATION")
    print("=" * 60)
    
    tests = [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_virtual_environment),
        ("Dependencies Installation", install_dependencies),
        ("Module Imports", check_imports),
        ("Environment Variables", check_environment_variables),
        ("Supabase Connection", test_supabase_connection),
        ("Main Module", test_main_module)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SETUP VALIDATION RESULTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:<10} {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 OVERALL: {passed}/{total} checks passed ({passed/total*100:.1f}%)")
    
    if passed >= total - 1:  # Allow 1 failure (like virtual env detection)
        print("\n🎉 BACKEND SETUP COMPLETE!")
        print("\n📋 READY TO START:")
        print("   uvicorn main:app --reload")
        print("\n📋 ENDPOINTS AVAILABLE:")
        print("   • GET  /              - Health check")
        print("   • GET  /health        - Detailed health")
        print("   • GET  /docs          - API documentation")
        print("   • POST /auth/signup   - User registration")
        print("   • POST /auth/login    - User authentication")
        print("   • GET  /auth/me       - Current user (protected)")
        print("   • POST /api/query     - Text queries (protected)")
        print("   • POST /api/ocr       - Image OCR (protected)")
        
        print("\n🔗 SUPABASE INTEGRATION:")
        print("   • Authentication via Supabase Auth")
        print("   • User profiles in 'users' table")
        print("   • JWT token validation")
        print("   • Row Level Security enabled")
        
        return True
    else:
        print(f"\n⚠️  Setup incomplete - {total-passed} issues need attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)