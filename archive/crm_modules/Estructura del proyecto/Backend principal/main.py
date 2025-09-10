from fastapi import FastAPI
from app.database import engine, Base
from app.routes import users, clients, opportunities, tasks, invoices, analytics

app = FastAPI(title="CRM Completo")

# Crear las tablas
Base.metadata.create_all(bind=engine)

# Rutas
app.include_router(users.router, prefix="/users", tags=["Usuarios"])
app.include_router(clients.router, prefix="/clients", tags=["Clientes"])
app.include_router(opportunities.router, prefix="/opportunities", tags=["Oportunidades"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tareas"])
app.include_router(invoices.router, prefix="/invoices", tags=["Facturación"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
