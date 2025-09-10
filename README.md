# Proyecto CRM - Backend Setup

## Backend Authentication Server

This backend server is implemented using FastAPI to handle user authentication for the CRM project.

### Features

- POST `/users/token` endpoint for user login.
- Verifies user credentials against SQLite database `crm.db`.
- Generates JWT access tokens on successful login.
- CORS enabled for frontend communication.
- Modular and extensible structure.

### Setup Instructions

1. Create and activate a Python virtual environment:

```bash
python -m venv venv
source venv/Scripts/activate  # Windows
# or
source venv/bin/activate      # Linux/macOS
```

2. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Run the backend server:

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

4. The backend will be available at `http://localhost:8000`.

### Notes

- Ensure the SQLite database `crm.db` is in the backend directory or update the path accordingly.
- The secret key for JWT in `backend/app/main.py` should be changed to a secure value in production.
- The frontend expects the login endpoint at `/users/token` on this backend.

### Troubleshooting

- If you get connection errors, verify the backend server is running and accessible.
- Check logs for detailed error messages.

---

This completes the backend authentication implementation to fix the login error and support the full project.
