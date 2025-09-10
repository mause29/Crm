def test_create_client(client, auth_headers):
    response = client.post(
        "/clients/",
        data={
            "name": "New Client",
            "email": "newclient@example.com",
            "phone": "1234567890"
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["msg"] == "Client created"

def test_get_clients(client, auth_headers):
    response = client.get("/clients/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_duplicate_client(client, auth_headers):
    # First create a client
    client.post(
        "/clients/",
        data={
            "name": "Test Client",
            "email": "duplicate@example.com",
            "phone": "1234567890"
        },
        headers=auth_headers
    )

    # Try to create the same client again
    response = client.post(
        "/clients/",
        data={
            "name": "Test Client 2",
            "email": "duplicate@example.com",
            "phone": "0987654321"
        },
        headers=auth_headers
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]
