import hashlib
import os

def generate_api_key():
    return hashlib.sha256(os.urandom(64)).hexdigest()

def verify_api_key(api_key, valid_keys):
    return api_key in valid_keys

def mask_sensitive_data(data):
    if isinstance(data, str) and len(data) > 4:
        return '*'*(len(data)-4) + data[-4:]
    return data
