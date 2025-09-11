from fastapi import FastAPI, HTTPException, Depends, status, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
import socketio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import authentication functions
from app.auth import create_access_token, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.database_new import get_db
from app.models import User
from verify_password import verify_password

# Import routers
from .routes.users import router as users_router
from .routes.gamification import router as gamification_router
from .routes.reports import router as reports_router
from .routes.clientes import router as clientes_router
from .routes.oportunidades import router as oportunidades_router
from .routes.tasks import router as tasks_router
from .routes.facturas import router as facturas_router
from .routes.notifications import router as notifications_router
from .routes.dashboard import router as dashboard_router
from .routes.email import router as email_router
from .routes.analytics import router as analytics_router

# Socket.IO setup
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=['http://localhost:5173', 'http://localhost:5174', 'http://localhost:3000', 'http://127.0.0.1:3000', 'https://localhost:3000', 'https://127.0.0.1:3000', 'http://localhost:8000'],
    cors_credentials=True
)

app = FastAPI()

# Allow CORS for frontend running on localhost:5173 (adjust if needed)
origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Token(BaseModel):
    access_token: str
    token_type: str

# Authentication functions are now handled by the users router

# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def message(sid, data):
    print(f"Message from {sid}: {data}")
    await sio.emit('message', data)

@sio.event
async def dashboard_update(sid, data):
    """Handle dashboard real-time updates"""
    print(f"Dashboard update from {sid}: {data}")
    await sio.emit('dashboard_updated', data)

@sio.event
async def notification(sid, data):
    """Handle real-time notifications"""
    print(f"Notification from {sid}: {data}")
    await sio.emit('notification_received', data)

# Include routers
app.include_router(users_router)
app.include_router(gamification_router)
app.include_router(reports_router)
app.include_router(clientes_router)
app.include_router(oportunidades_router)
app.include_router(tasks_router)
app.include_router(facturas_router)
app.include_router(notifications_router)
app.include_router(dashboard_router)
app.include_router(email_router)
app.include_router(analytics_router)

# Create combined ASGI app for Socket.IO and FastAPI
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(socket_app, host="0.0.0.0", port=8000)
