from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp
import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
db = SQLAlchemy(app)

# Modelo de usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    twofa_secret = db.Column(db.String(16), nullable=True)
    role = db.Column(db.String(50), default='user')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Crear 2FA
def generate_2fa_secret():
    return pyotp.random_base32()

# Verificar 2FA
def verify_2fa(secret, token):
    totp = pyotp.TOTP(secret)
    return totp.verify(token)

# Encriptar contraseña
def hash_password(password):
    return generate_password_hash(password)

# Verificar contraseña
def verify_password(hashed_password, password):
    return check_password_hash(hashed_password, password)

# Log de auditoría
class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
