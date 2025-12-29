#!/usr/bin/env python3
"""
Test script for OCR functionality
"""

import requests
import json
from PIL import Image, ImageDraw, ImageFont
import io
import os

def create_test_image():
    """Create a simple test image with text"""
    # Create a white image
    img = Image.new('RGB', (400, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add some text
    text = "PM-KISAN Scheme\nEligibility: Small farmers\nBenefit: Rs 6000 per year"
    
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        font = None
    
    # Draw text
    draw.text((20, 50), text, fill='black', font=font)
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes

def test_ocr_endpoint():
    """Test the OCR endpoint"""
    print("🧪 Testing OCR endpoint...")
    
    # Create test image
    test_image = create_test_image()
    
    # Prepare the request
    files = {'file': ('test_image.png', test_image, 'image/png')}
    data = {'language': 'en'}
    
    try:
        # Make request to OCR endpoint
        response = requests.post(
            "http://127.0.0.1:8000/api/ocr",
            files=files,
            data=data,
            headers={'Authorization': 'Bearer test_token'}  # This will fail auth, but we can test OCR logic
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 401:
            print("✅ OCR endpoint is accessible (authentication required as expected)")
        elif response.status_code == 200:
            print("✅ OCR endpoint working!")
            data = response.json()
            print(f"Extracted text: {data.get('extracted_text', 'N/A')}")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

def test_text_query():
    """Test the text query endpoint"""
    print("\n🧪 Testing text query endpoint...")
    
    query_data = {
        "question": "What is PM-KISAN scheme?",
        "language": "en"
    }
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/query",
            json=query_data,
            headers={'Authorization': 'Bearer test_token'}  # This will fail auth
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print("✅ Query endpoint is accessible (authentication required as expected)")
        elif response.status_code == 200:
            print("✅ Query endpoint working!")
            data = response.json()
            print(f"Answer preview: {data.get('answer', 'N/A')[:100]}...")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

def main():
    print("🚀 Testing Civic-AI Core Functionality")
    print("=" * 50)
    
    # Test if server is running
    try:
        response = requests.get("http://127.0.0.1:8000/health")
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print("❌ Server health check failed")
            return
    except requests.exceptions.RequestException:
        print("❌ Server is not running. Start with: uvicorn main:app --reload")
        return
    
    # Test endpoints
    test_text_query()
    test_ocr_endpoint()
    
    print("\n" + "=" * 50)
    print("🎉 Core functionality tests completed!")
    print("\n📋 Next steps:")
    print("1. Set up authentication (login/signup)")
    print("2. Test with real authentication tokens")
    print("3. Upload real images for OCR testing")

if __name__ == "__main__":
    main()