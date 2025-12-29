#!/usr/bin/env python3
"""
Test script for Civic-AI authentication endpoints
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_signup():
    """Test user signup"""
    print("🧪 Testing signup...")
    
    signup_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
        
        if response.status_code == 200:
            print("✅ Signup successful")
            data = response.json()
            return data.get("access_token")
        else:
            print(f"❌ Signup failed: {response.status_code} - {response.text}")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Signup request failed: {e}")
        return None

def test_login():
    """Test user login"""
    print("🧪 Testing login...")
    
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        
        if response.status_code == 200:
            print("✅ Login successful")
            data = response.json()
            return data.get("access_token")
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Login request failed: {e}")
        return None

def test_protected_route(token):
    """Test protected route with token"""
    print("🧪 Testing protected route...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        
        if response.status_code == 200:
            print("✅ Protected route access successful")
            data = response.json()
            print(f"   User: {data.get('name')} ({data.get('email')})")
            return True
        else:
            print(f"❌ Protected route failed: {response.status_code} - {response.text}")
            return False
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Protected route request failed: {e}")
        return False

def test_query_endpoint(token):
    """Test the protected query endpoint"""
    print("🧪 Testing protected query endpoint...")
    
    headers = {"Authorization": f"Bearer {token}"}
    query_data = {
        "question": "What is PM-KISAN scheme?",
        "language": "en"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/query", json=query_data, headers=headers)
        
        if response.status_code == 200:
            print("✅ Query endpoint successful")
            data = response.json()
            print(f"   Response includes user_id: {'user_id' in data}")
            return True
        else:
            print(f"❌ Query endpoint failed: {response.status_code} - {response.text}")
            return False
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Query endpoint request failed: {e}")
        return False

def main():
    print("🚀 Testing Civic-AI Authentication System")
    print("=" * 50)
    
    # Test server is running
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("❌ Server is not running. Start with: uvicorn main:app --reload")
            sys.exit(1)
        print("✅ Server is running")
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to server. Start with: uvicorn main:app --reload")
        sys.exit(1)
    
    # Test signup (might fail if user already exists)
    token = test_signup()
    
    # If signup fails, try login
    if not token:
        print("Signup failed, trying login...")
        token = test_login()
    
    if not token:
        print("❌ Could not get access token")
        sys.exit(1)
    
    # Test protected routes
    if not test_protected_route(token):
        sys.exit(1)
    
    if not test_query_endpoint(token):
        sys.exit(1)
    
    print("\n🎉 All authentication tests passed!")
    print("\n📋 Authentication system is ready for frontend integration")

if __name__ == "__main__":
    main()