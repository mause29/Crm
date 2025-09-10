import time
import sys
import os
import pytest
from fastapi.testclient import TestClient

# Adjust sys.path to import app modules correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend', 'app')))

from main_new import app
from utils.security import rate_limit_check, log_security_event

client = TestClient(app)

def test_rate_limit_check_basic():
    identifier = "test_ip"
    # Clear previous state
    if hasattr(rate_limit_check, "_requests"):
        rate_limit_check._requests.clear()

    # Allow up to 5 requests in 60 seconds
    for _ in range(5):
        assert rate_limit_check(identifier, max_requests=5, window_seconds=60) is True

    # 6th request should be blocked
    assert rate_limit_check(identifier, max_requests=5, window_seconds=60) is False

def test_rate_limit_reset():
    identifier = "test_ip_reset"
    if hasattr(rate_limit_check, "_requests"):
        rate_limit_check._requests.clear()

    # Fill requests
    for _ in range(5):
        assert rate_limit_check(identifier, max_requests=5, window_seconds=1) is True

    # Wait for window to expire
    time.sleep(1.1)

    # Should allow requests again
    assert rate_limit_check(identifier, max_requests=5, window_seconds=1) is True

def test_login_rate_limit_endpoint():
    # Simulate multiple login attempts to test rate limiting on /users/token
    for _ in range(10):
        response = client.post("/users/token", data={"username": "admin@crm.com", "password": "admin123"})
        assert response.status_code == 200 or response.status_code == 429

    # 11th attempt should be rate limited
    response = client.post("/users/token", data={"username": "admin@crm.com", "password": "admin123"})
    assert response.status_code == 429
