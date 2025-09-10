import asyncio
import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=['http://localhost:5173', 'http://localhost:5174'], cors_credentials=True)
app = FastAPI()
sio_app = socketio.ASGIApp(sio, other_asgi_app=app)

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

# To run this socket server, use:
# uvicorn backend.app.socket_server:sio_app --reload --host 0.0.0.0 --port 8001
