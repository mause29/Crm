from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Empresa / Tenant
class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Relación usuario / tenant
class TenantUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'))
    user_id = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(50), default='user')
