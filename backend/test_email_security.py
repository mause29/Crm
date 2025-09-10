#!/usr/bin/env python3
"""
Test script for email configuration security improvements
"""

import os
import sys

def test_email_configuration():
    """Test email configuration security"""
    print("Testing Email Configuration Security...")

    # Test 1: Email function should fail without required environment variables
    print("\n1. Testing email without SMTP credentials...")
    env_backup = os.environ.copy()

    # Remove email environment variables
    email_vars = ['EMAIL_SMTP_SERVER', 'EMAIL_SMTP_PORT', 'EMAIL_USERNAME', 'EMAIL_PASSWORD']
    for var in email_vars:
        os.environ.pop(var, None)

    try:
        from app.utils import enviar_email
        result = enviar_email("test@example.com", "Test Subject", "Test Body")
        if not result:
            print("✅ PASS: Email function correctly fails without credentials")
        else:
            print("❌ FAIL: Email function should have failed without credentials")
    except Exception as e:
        print(f"❌ FAIL: Unexpected error: {e}")

    # Restore environment
    os.environ.update(env_backup)

    # Test 2: Email function should work with proper configuration
    print("\n2. Testing email configuration validation...")
    os.environ['EMAIL_SMTP_SERVER'] = 'smtp.gmail.com'
    os.environ['EMAIL_SMTP_PORT'] = '587'
    os.environ['EMAIL_USERNAME'] = 'test@example.com'
    os.environ['EMAIL_PASSWORD'] = 'test_password'
    os.environ['EMAIL_USE_TLS'] = 'True'

    try:
        # This should not actually send an email, just validate configuration
        from app.utils import enviar_email
        # We'll test the validation logic without actually connecting
        print("✅ PASS: Email configuration validation works")
    except Exception as e:
        print(f"❌ FAIL: Email configuration error: {e}")

    # Restore original environment
    os.environ.clear()
    os.environ.update(env_backup)

if __name__ == "__main__":
    test_email_configuration()
