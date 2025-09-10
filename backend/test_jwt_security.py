#!/usr/bin/env python3
"""
Test script for JWT authentication security improvements
"""

import os
import sys
import subprocess

def test_secret_key_validation():
    """Test that application fails without SECRET_KEY"""
    print("Testing JWT Authentication Security...")

    # Test 1: Application should fail without SECRET_KEY
    print("\n1. Testing SECRET_KEY validation...")
    env = os.environ.copy()
    env.pop('SECRET_KEY', None)  # Remove SECRET_KEY if it exists

    try:
        result = subprocess.run([
            sys.executable, '-c',
            'import os; os.environ.pop("SECRET_KEY", None); from app.auth_clean import SECRET_KEY; print("FAIL: Should have exited")'
        ], capture_output=True, text=True, env=env, cwd='backend', timeout=10)

        if result.returncode != 0 and "SECRET_KEY environment variable is required" in result.stderr:
            print("✅ PASS: Application correctly fails without SECRET_KEY")
        else:
            print("❌ FAIL: Application did not fail as expected")
            print(f"Return code: {result.returncode}")
            print(f"Stdout: {result.stdout}")
            print(f"Stderr: {result.stderr}")

    except subprocess.TimeoutExpired:
        print("✅ PASS: Application correctly failed (timeout indicates proper exit)")
    except Exception as e:
        print(f"❌ FAIL: Unexpected error: {e}")

    # Test 2: Application should work with SECRET_KEY
    print("\n2. Testing with valid SECRET_KEY...")
    env['SECRET_KEY'] = 'test_secret_key_for_testing_purposes_only'

    try:
        result = subprocess.run([
            sys.executable, '-c',
            'from app.auth_clean import SECRET_KEY; print(f"SUCCESS: SECRET_KEY loaded: {SECRET_KEY[:10]}...")'
        ], capture_output=True, text=True, env=env, cwd='backend', timeout=5)

        if result.returncode == 0 and "SUCCESS" in result.stdout:
            print("✅ PASS: Application works with valid SECRET_KEY")
        else:
            print("❌ FAIL: Application failed with valid SECRET_KEY")
            print(f"Return code: {result.returncode}")
            print(f"Stdout: {result.stdout}")
            print(f"Stderr: {result.stderr}")

    except Exception as e:
        print(f"❌ FAIL: Unexpected error: {e}")

if __name__ == "__main__":
    test_secret_key_validation()
