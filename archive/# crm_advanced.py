# crm_advanced.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime, timedelta
import jwt
import hashlib
import smtplib
from email.mime.text import MIMEText
import random
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from typing import List
import asyncio

# ========================
# Configuración básica
# ========================
DATABASE_URL = "sqlite:///./crm.db"
SECRET_KEY = "supersecretkey"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================
# Modelos de BD
# ========================
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    two_fa_enabled = Column(Boolean, default=False)
    points = Column(Integer, default=0)
    last_login = Column(DateTime, default=datetime.utcnow)

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    vip_status = Column(Boolean, default=False)
    last_interaction = Column(DateTime, default=datetime.utcnow)

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    amount = Column(Float)
    due_date = Column(DateTime)
    paid = Column(Boolean, default=False)
    client = relationship("Client")

class Contract(Base):
    __tablename__ = "contracts"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    document_url = Column(String)
    version = Column(Integer, default=1)
    signed = Column(Boolean, default=False)
    client = relationship("Client")

Base.metadata.create_all(bind=engine)

# ========================
# Seguridad avanzada
# ========================
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str):
    return hash_password(password) == hashed

def create_token(user_id: int):
    payload = {"user_id": user_id, "exp": datetime.utcnow() + timedelta(hours=12)}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# ========================
# Gamificación
# ========================
def add_points(user_id: int, points: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.points += points
        db.commit()
    db.close()

# ========================
# Inteligencia y ML
# ========================
def predict_churn(client_data: pd.DataFrame):
    # Modelo dummy
    X = client_data.drop(columns=["client_id"])
    y = np.random.randint(0, 2, len(client_data))
    model = RandomForestClassifier()
    model.fit(X, y)
    return model.predict_proba(X)[:,1]

# ========================
# Facturación avanzada
# ========================
@app.post("/invoice/pay/{invoice_id}")
def pay_invoice(invoice_id: int, card_number: str, exp_date: str, cvv: str):
    db = SessionLocal()
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    # Aquí integrarías PayPal con card checkout
    invoice.paid = True
    db.commit()
    db.close()
    return {"status": "success", "invoice_id": invoice_id}

# ========================
# Reporting y Analytics
# ========================
@app.get("/dashboard/kpi")
def dashboard_kpi():
    db = SessionLocal()
    total_clients = db.query(Client).count()
    total_invoices = db.query(Invoice).count()
    paid_invoices = db.query(Invoice).filter(Invoice.paid == True).count()
    db.close()
    return {
        "total_clients": total_clients,
        "total_invoices": total_invoices,
        "paid_invoices": paid_invoices,
        "payment_rate": round(paid_invoices/total_invoices*100 if total_invoices else 0, 2)
    }

# ========================
# Chatbot / Inteligencia conversacional
# ========================
async def send_automatic_message(client_email: str, message: str):
    # Aquí se podría integrar WhatsApp, email o SMS
    msg = MIMEText(message)
    msg["Subject"] = "CRM Notification"
    msg["From"] = "crm@example.com"
    msg["To"] = client_email
    # Dummy: enviar email
    print(f"Enviando mensaje a {client_email}: {message}")

# ========================
# Multi-tenant / SaaS
# ========================
# Cada empresa tendría su propia DB (conceptual)
tenants = {}

def get_tenant_db(tenant_id: str):
    if tenant_id not in tenants:
        tenants[tenant_id] = f"sqlite:///./crm_{tenant_id}.db"
    return tenants[tenant_id]

# ========================
# Optimización móvil
# ========================
@app.get("/mobile/notifications/{user_id}")
def get_notifications(user_id: int):
    # Retorna notificaciones push para app móvil
    return [{"message": "Tarea vencida", "timestamp": datetime.utcnow()}]

# ========================
# Escalabilidad y DevOps
# ========================
# Concepto: se usaría Docker, Kubernetes y backups automáticos
def backup_db(db_url: str):
    print(f"Respaldando base de datos {db_url}...")

# ========================
# Main
# ========================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
