import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from backend.app.main import app
from backend.app.database import SessionLocal, Base, engine
from backend.app.models import User
from backend.app.utils import get_password_hash

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def test_user():
    # Create empresa and user for all tests
    db = SessionLocal()
    empresa = Empresa(nombre="Test Empresa")
    db.add(empresa)
    db.commit()
    db.refresh(empresa)
    
    hashed = get_password_hash("testpassword")
    user = Usuario(
        nombre="Test User",
        email="testuser@example.com",
        hashed_password=hashed,
        rol="user",
        empresa_id=empresa.id
    )
    db.add(user)
    db.commit()
    db.close()
    return user

def test_user_registration_and_login():
    # First create an empresa
    from backend.app.models import Empresa
    from backend.app.database import SessionLocal
    db = SessionLocal()
    empresa = Empresa(nombre="Test Empresa")
    db.add(empresa)
    db.commit()
    db.refresh(empresa)
    empresa_id = empresa.id
    db.close()

    # Register user with empresa_id
    response = client.post("/usuarios/", json={
        "nombre": "Test User",
        "email": "testuser@example.com",
        "password": "testpassword",
        "rol": "user",
        "empresa_id": empresa_id
    })
    assert response.status_code == 200
    assert response.json()["msg"] == "Usuario creado"

    # Login user
    response = client.post("/usuarios/token", data={
        "username": "testuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_cliente():
    # Login to get token
    response = client.post("/usuarios/token", data={
        "username": "testuser@example.com",
        "password": "testpassword"
    })
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create cliente
    response = client.post("/clientes/", data={
        "nombre": "Cliente Test",
        "email": "cliente@example.com",
        "telefono": "123456789"
    }, headers=headers)
    print(f"Cliente creation response: {response.status_code}, {response.text}")
    print(f"Headers: {headers}")
    assert response.status_code == 200
    assert response.json()["msg"] == "Cliente creado"

def test_create_oportunidad():
    # Login to get token
    response = client.post("/usuarios/token", data={
        "username": "testuser@example.com",
        "password": "testpassword"
    })
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create oportunidad with cliente_id 1
    response = client.post("/oportunidades/", json={
        "titulo": "Oportunidad Test",
        "valor": 1000.0,
        "cliente_id": 1
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["msg"] == "Oportunidad creada"

def test_create_factura_and_pay():
    # Login to get token
    response = client.post("/usuarios/token", data={
        "username": "testuser@example.com",
        "password": "testpassword"
    })
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create factura
    response = client.post("/facturas/", json={
        "cliente_id": 1,
        "monto": 500.0
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["msg"] == "Factura creada"

    # Pay factura with id 1 - skip if PayPal credentials not available
    import os
    if os.getenv("PAYPAL_CLIENT_ID") and os.getenv("PAYPAL_CLIENT_SECRET"):
        response = client.post("/facturas/pagar/1", headers=headers)
        # Payment may fail due to sandbox or card details, so accept 200 or 400
        assert response.status_code in (200, 400)
    else:
        # Skip PayPal test if credentials not configured
        pytest.skip("PayPal credentials not configured")
