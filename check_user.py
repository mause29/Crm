import sqlite3

def check_user(email):
    conn = sqlite3.connect('crm.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, name FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()
    if user:
        print(f"User found: ID={user[0]}, Email={user[1]}, Name={user[2]}")
    else:
        print("User not found")

if __name__ == "__main__":
    check_user("admin@crm.com")
