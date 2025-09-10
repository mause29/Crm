#!/usr/bin/env python3
"""
Test script for security headers middleware
"""

import os
import sys
from fastapi.testclient import TestClient

def test_security_headers():
    """Test security headers middleware"""
    print("Testing Security Headers Middleware...")

    try:
        # Import the FastAPI app
        from app.main import app

        # Create test client
        client = TestClient(app)

        # Test 1: Check health endpoint for security headers
        print("\n1. Testing security headers on /health endpoint...")
        response = client.get("/health")

        # Check for essential security headers
        security_headers = [
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "X-XSS-Protection",
            "Referrer-Policy"
        ]

        missing_headers = []
        for header in security_headers:
            if header not in response.headers:
                missing_headers.append(header)

        if not missing_headers:
            print("✅ PASS: All essential security headers are present")
        else:
            print(f"❌ FAIL: Missing security headers: {missing_headers}")

        # Test 2: Check CSP header content
        print("\n2. Testing Content Security Policy...")
        csp = response.headers.get("Content-Security-Policy", "")
        if csp and "default-src 'self'" in csp:
            print("✅ PASS: CSP header contains expected directives")
        else:
            print("❌ FAIL: CSP header is missing or incomplete")

        # Test 3: Check HSTS header
        print("\n3. Testing HTTP Strict Transport Security...")
        hsts = response.headers.get("Strict-Transport-Security", "")
        if hsts and "max-age=31536000" in hsts:
            print("✅ PASS: HSTS header is properly configured")
        else:
            print("❌ FAIL: HSTS header is missing or misconfigured")

        # Test 4: Check rate limiting (make multiple requests)
        print("\n4. Testing rate limiting...")
        responses = []
        for i in range(65):  # Exceed the 60 requests per minute limit
            resp = client.get("/health")
            responses.append(resp.status_code)

        rate_limited_responses = [r for r in responses if r == 429]
        if rate_limited_responses:
            print("✅ PASS: Rate limiting is working (received 429 status codes)")
        else:
            print("❌ FAIL: Rate limiting may not be working properly")

        print(f"\n   Total requests: {len(responses)}")
        print(f"   Rate limited responses: {len(rate_limited_responses)}")

    except Exception as e:
        print(f"❌ FAIL: Error testing security headers: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_security_headers()
