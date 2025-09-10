#!/usr/bin/env python3
"""
Test script to verify critical CRM features are working
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_server_health():
    """Test if server is running"""
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ Server is running and accessible")
            return True
        else:
            print(f"❌ Server responded with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return False

def test_openapi_docs():
    """Test if OpenAPI docs are accessible"""
    try:
        response = requests.get(f"{BASE_URL}/openapi.json")
        if response.status_code == 200:
            print("✅ OpenAPI documentation is accessible")
            return True
        else:
            print(f"❌ OpenAPI docs responded with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot access OpenAPI docs: {e}")
        return False

def test_rate_limiting():
    """Test rate limiting middleware"""
    print("Testing rate limiting...")
    for i in range(105):  # More than 100 requests per minute
        try:
            response = requests.get(f"{BASE_URL}/docs")
            if response.status_code == 429:
                print("✅ Rate limiting is working correctly")
                return True
        except:
            pass
    print("❌ Rate limiting may not be working")
    return False

def test_security_headers():
    """Test security headers"""
    try:
        response = requests.get(f"{BASE_URL}/docs")
        headers = response.headers

        security_headers = [
            'X-Content-Type-Options',
            'X-Frame-Options',
            'X-XSS-Protection',
            'Strict-Transport-Security',
            'Content-Security-Policy'
        ]

        found_headers = [h for h in security_headers if h in headers]
        if len(found_headers) >= 3:
            print(f"✅ Security headers present: {found_headers}")
            return True
        else:
            print(f"❌ Missing security headers. Found: {found_headers}")
            return False
    except Exception as e:
        print(f"❌ Error testing security headers: {e}")
        return False

def main():
    print("🔍 Testing CRM System Critical Features")
    print("=" * 50)

    tests = [
        ("Server Health", test_server_health),
        ("OpenAPI Documentation", test_openapi_docs),
        ("Security Headers", test_security_headers),
        ("Rate Limiting", test_rate_limiting),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        if test_func():
            passed += 1
        time.sleep(0.1)  # Small delay between tests

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All critical features are working!")
        return True
    else:
        print("⚠️  Some features need attention")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
