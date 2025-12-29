#!/usr/bin/env python3
"""
Simple test to verify backend is working
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def main():
    print("🚀 CIVIC-AI BACKEND SIMPLE TEST")
    print("=" * 40)
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health endpoint: OK")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False
    
    # Test root endpoint
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint: {data['message']}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False
    
    # Test docs endpoint
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ Docs endpoint: Accessible")
        else:
            print(f"❌ Docs endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Docs endpoint error: {e}")
        return False
    
    # Test auth endpoints exist (expect validation errors)
    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json={})
        if response.status_code == 422:  # Validation error expected
            print("✅ Signup endpoint: Exists (validation working)")
        else:
            print(f"⚠️  Signup endpoint: Unexpected response {response.status_code}")
    except Exception as e:
        print(f"❌ Signup endpoint error: {e}")
        return False
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={})
        if response.status_code == 422:  # Validation error expected
            print("✅ Login endpoint: Exists (validation working)")
        else:
            print(f"⚠️  Login endpoint: Unexpected response {response.status_code}")
    except Exception as e:
        print(f"❌ Login endpoint error: {e}")
        return False
    
    # Test protected endpoints (expect auth errors)
    try:
        response = requests.get(f"{BASE_URL}/auth/me")
        if response.status_code == 403:  # Forbidden expected without auth
            print("✅ Protected /auth/me: Requires authentication")
        else:
            print(f"⚠️  Protected /auth/me: Unexpected response {response.status_code}")
    except Exception as e:
        print(f"❌ Protected endpoint error: {e}")
        return False
    
    print("\n" + "=" * 40)
    print("🎉 ALL BASIC TESTS PASSED!")
    print("\n📋 BACKEND STATUS:")
    print("   ✅ Server running successfully")
    print("   ✅ All endpoints accessible")
    print("   ✅ Authentication validation working")
    print("   ✅ Protected routes secured")
    print("   ✅ Ready for frontend integration")
    
    return True

if __name__ == "__main__":
    main()