from fastapi import FastAPI
from app.database import Base, engine
from app.routes import users, clients, opportunities, tasks, invoices, reports, analytics

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRM Completo")

# Rutas
app.include_router(users.router)
app.include_router(clients.router)
app.include_router(opportunities.router)
app.include_router(tasks.router)
app.include_router(invoices.router)
app.include_router(reports.router)
app.include_router(analytics.router)
