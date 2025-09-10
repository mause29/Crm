import sqlite3
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_hashed_password(email):
    conn = sqlite3.connect('crm.db')
    cursor = conn.cursor()
    cursor.execute("SELECT hashed_password FROM users WHERE email=?", (email,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

if __name__ == "__main__":
    email = "admin@crm.com"
    password = "admin123"
    hashed = get_hashed_password(email)
    if hashed:
        if verify_password(password, hashed):
            print("Password is correct")
        else:
            print("Password is incorrect")
    else:
        print("User not found")
