from flask import Blueprint, request, jsonify
from app import db
from models import User
from utils.jwt_util import create_token, token_required
from utils.security import send_2fa_code, verify_2fa_code

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    user = User(email=data['email'], role=data.get('role', 'user'))
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg':'User registered'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        if user.two_fa_enabled:
            send_2fa_code(user)
            return jsonify({'2fa': True, 'msg':'Enter 2FA code'}), 200
        token = create_token(user.id)
        return jsonify({'token': token})
    return jsonify({'msg':'Invalid credentials'}), 401

@auth_bp.route('/verify-2fa', methods=['POST'])
def verify_2fa():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and verify_2fa_code(user, data['code']):
        token = create_token(user.id)
        return jsonify({'token': token})
    return jsonify({'msg':'Invalid 2FA code'}), 401
