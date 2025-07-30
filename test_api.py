#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:8080"

def test_api():
    print("Testing VidelizerAI API...")
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Server is running: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running on port 8080")
        return
    
    # Test 2: Test upload endpoint
    try:
        # Create a fake file for testing
        files = {'video': ('test.mp4', b'fake video content', 'video/mp4')}
        response = requests.post(f"{BASE_URL}/api/videos/upload", files=files)
        print(f"✅ Upload endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
    except Exception as e:
        print(f"❌ Upload endpoint error: {e}")
    
    # Test 3: Test analysis endpoint
    try:
        data = {"videoId": "test-video-id", "options": {}}
        response = requests.post(f"{BASE_URL}/api/videos/analyze", json=data)
        print(f"✅ Analysis endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
    except Exception as e:
        print(f"❌ Analysis endpoint error: {e}")
    
    # Test 4: Test analysis status endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/analysis/test-analysis-id")
        print(f"✅ Analysis status endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {json.dumps(data, indent=2)}")
    except Exception as e:
        print(f"❌ Analysis status endpoint error: {e}")

if __name__ == "__main__":
    test_api() 