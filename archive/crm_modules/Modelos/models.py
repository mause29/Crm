from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(50))
    company_id = db.Column(db.Integer)
    two_fa_enabled = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    company_id = db.Column(db.Integer)

class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    title = db.Column(db.String(150))
    amount = db.Column(db.Float)
    status = db.Column(db.String(50))
    probability = db.Column(db.Float)
    close_date = db.Column(db.DateTime)
    company_id = db.Column(db.Integer)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.id'))
    title = db.Column(db.String(150))
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    company_id = db.Column(db.Integer)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    amount = db.Column(db.Float)
    status = db.Column(db.String(50), default='Pending')
    due_date = db.Column(db.DateTime)
    company_id = db.Column(db.Integer)
    paypal_payment_id = db.Column(db.String(120))
