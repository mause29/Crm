from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database_new import Base, engine
from .routes import (
    users_paginated as users,  # Usar la versión optimizada con paginación
    clientes,
    oportunidades,
    facturas,
    gamification,
    notifications,
    reports_new as reports,
    tasks,
    analytics,
    dashboard,
    email,
    filtering,
    monitoring
)
from .middleware.security import add_security_middleware
from .middleware.https import add_https_middleware
from .middleware.security_headers import SecurityHeadersMiddleware, rate_limit_middleware
from .middleware.api_monitoring import add_api_monitoring_middleware
from .services.scheduler_service import start_scheduler, stop_scheduler
from .utils.performance import performance_monitor, get_performance_stats
from .utils.cache import cache_manager
from .config.settings import settings
import socketio
import uvicorn
import asyncio

app = FastAPI(
    title="CRM Completo con PayPal y ML",
    description="""
    # Sistema Completo de CRM con Gamificación

    Un sistema avanzado de gestión de relaciones con clientes que incluye:

    ## 🚀 Características Principales

    ### Gestión de Clientes y Ventas
    - **Clientes**: Gestión completa de base de datos de clientes
    - **Oportunidades**: Seguimiento de oportunidades de venta
    - **Facturas**: Generación y gestión de facturas con PayPal

    ### Gamificación y Motivación
    - **Logros**: Sistema de badges y puntos para motivar a los usuarios
    - **Notificaciones**: Alertas en tiempo real vía Socket.IO
    - **Dashboard**: Métricas y reportes visuales

    ### Seguridad y Autenticación
    - **JWT**: Autenticación segura con tokens
    - **2FA**: Autenticación de dos factores opcional
    - **Roles**: Control de acceso basado en roles (user, manager, admin)

    ### Integraciones
    - **PayPal**: Procesamiento de pagos
    - **Email**: Automatización de correos
    - **Analytics**: Análisis de datos y machine learning básico

    ## 📚 Documentación de la API

    Esta API está documentada usando OpenAPI 3.0. Puedes acceder a la documentación interactiva en `/docs` o `/redoc`.

    ### Autenticación
    La mayoría de los endpoints requieren autenticación JWT. Incluye el token en el header:
    ```
    Authorization: Bearer <tu_token>
    ```

    ### Ejemplos de Uso
    Consulta los ejemplos en cada endpoint para entender cómo usar la API.
    """,
    version="1.0.0",
    contact={
        "name": "CRM Support",
        "email": "support@crm.com",
    },
    license_info={
        "name": "MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://localhost:3000",
        "https://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "X-Requested-With",
        "Accept",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
        "X-CSRF-Token"
    ],
    allow_credentials=True,
    max_age=86400,  # 24 hours
)

# Add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)

# Add rate limiting middleware
app.middleware("http")(rate_limit_middleware)

# Add security middleware
add_security_middleware(app)

# Add HTTPS middleware with redirect disabled for development and HSTS enabled
add_https_middleware(app, enable_redirect=False, https_port=443, enable_hsts=True)

# Add API monitoring middleware
add_api_monitoring_middleware(app)

# Include all routers
app.include_router(users.router)
app.include_router(clientes)
app.include_router(oportunidades)
app.include_router(facturas)
app.include_router(gamification)
app.include_router(notifications)
app.include_router(reports.router)
app.include_router(tasks)
app.include_router(analytics)
app.include_router(dashboard)
app.include_router(email)
app.include_router(filtering)
app.include_router(monitoring.router)

# Performance monitoring endpoint
@app.get("/performance/stats", tags=["performance"])
async def get_performance_statistics():
    """
    Obtiene estadísticas de rendimiento del sistema.

    **Permisos:** Solo administradores

    **Respuesta:**
    - system: Estadísticas del sistema (CPU, memoria, disco)
    - endpoints: Estadísticas de rendimiento por endpoint
    """
    return await get_performance_stats()

@app.get("/health", tags=["health"])
async def health_check():
    """
    Endpoint de verificación de salud del sistema.

    **Respuesta:**
    - status: Estado del sistema
    - timestamp: Timestamp de la verificación
    - version: Versión de la API
    """
    import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "performance": await get_performance_stats()
    }

# Socket.IO setup
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app_sio = socketio.ASGIApp(sio, other_asgi_app=app)

@app.on_event("startup")
async def startup_event():
    """Initialize database and seed initial data"""
    Base.metadata.create_all(bind=engine)

    # Start scheduler service
    start_scheduler()

    # Seed sample achievements
    from models import Achievement
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        if not db.query(Achievement).first():
            achievements = [
                Achievement(name="Primer Vendedor", description="Completa tu primera venta", points_required=50, badge_icon="🏆"),
                Achievement(name="Vendedor Estrella", description="Alcanza 1000 puntos", points_required=1000, badge_icon="⭐"),
                Achievement(name="Maestro de Ventas", description="Cierra 10 oportunidades", points_required=500, badge_icon="👑"),
                Achievement(name="Cliente Builder", description="Añade 5 clientes", points_required=150, badge_icon="👥"),
                Achievement(name="Task Master", description="Completa 10 tareas", points_required=200, badge_icon="✅"),
            ]
            for ach in achievements:
                db.add(ach)
            db.commit()
            print("Sample achievements seeded successfully")
    except Exception as e:
        print(f"Error seeding achievements: {e}")
        db.rollback()
    finally:
        db.close()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    stop_scheduler()
    print("Application shutdown complete")

@sio.event
async def connect(sid, environ):
    """Handle Socket.IO client connection"""
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    """Handle Socket.IO client disconnection"""
    print(f"Client disconnected: {sid}")

@sio.event
async def send_notification(sid, data):
    """Send notification to all connected clients"""
    await sio.emit('notification', data)
    print(f"Notification sent: {data}")

@sio.event
async def send_receive_notification(sid, data):
    """Send notification with receiveNotification event"""
    await sio.emit('receiveNotification', data)
    print(f"Receive notification sent: {data}")

@sio.event
async def join_room(sid, room):
    """Join a Socket.IO room"""
    sio.enter_room(sid, room)
    print(f"Client {sid} joined room: {room}")

@sio.event
async def leave_room(sid, room):
    """Leave a Socket.IO room"""
    sio.leave_room(sid, room)
    print(f"Client {sid} left room: {room}")

if __name__ == "__main__":
    uvicorn.run(app_sio, host="0.0.0.0", port=8000)
