import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("🧪 Testing CRM API Endpoints")
    print("=" * 50)

    # Test 1: Check if API is running
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ API Documentation accessible")
        else:
            print("❌ API Documentation not accessible")
    except Exception as e:
        print(f"❌ API not running: {e}")
        return

    # Test 2: Get users (should return empty list)
    try:
        response = requests.get(f"{BASE_URL}/users/")
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Users endpoint working - Found {len(users)} users")
        else:
            print(f"❌ Users endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Users endpoint error: {e}")

    # Test 3: Try to create a user
    try:
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "test123",
            "role": "user",
            "company_id": 1
        }
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        if response.status_code == 200:
            print("✅ User created successfully")
        else:
            print(f"❌ User creation failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ User creation error: {e}")

    # Test 4: Try to login
    try:
        login_data = {
            "username": "test@example.com",
            "password": "test123"
        }
        response = requests.post(f"{BASE_URL}/users/token", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Login successful - Token received")
            token = token_data.get("access_token")
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            token = None
    except Exception as e:
        print(f"❌ Login error: {e}")
        token = None

    # Test 5: Test protected endpoints with token
    if token:
        headers = {"Authorization": f"Bearer {token}"}

        # Test opportunities
        try:
            response = requests.get(f"{BASE_URL}/opportunities/", headers=headers)
            if response.status_code == 200:
                opportunities = response.json()
                print(f"✅ Opportunities endpoint working - Found {len(opportunities)} opportunities")
            else:
                print(f"❌ Opportunities endpoint failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Opportunities endpoint error: {e}")

        # Test clients
        try:
            response = requests.get(f"{BASE_URL}/clientes/", headers=headers)
            if response.status_code == 200:
                clients = response.json()
                print(f"✅ Clients endpoint working - Found {len(clients)} clients")
            else:
                print(f"❌ Clients endpoint failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Clients endpoint error: {e}")

    print("\n" + "=" * 50)
    print("🎉 API Testing Complete!")

if __name__ == "__main__":
    test_api()
