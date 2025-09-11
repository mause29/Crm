from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database_new import Base

class Company(Base):
    """
    Model that represents a company in the CRM system.

    A company can have multiple users and clients associated.
    Used to segment data by company in a multi-tenant environment.

    Attributes:
        id (int): Unique identifier of the company
        name (str): Name of the company
        users (relationship): Users belonging to this company
        clients (relationship): Clients belonging to this company
    """
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    users = relationship("User", backref="company")
    clients = relationship("Client", backref="company")

class User(Base):
    """
    Model that represents a user in the CRM system.

    Users can have different roles (user, admin, manager) and
    belong to a specific company.

    Attributes:
        id (int): Unique identifier of the user
        name (str): Full name of the user
        email (str): Unique email address
        hashed_password (str): Encrypted password
        role (str): Role of the user (user, admin, manager)
        is_active (bool): Account activation status
        two_factor_secret (str): Secret for two-factor authentication
        created_at (datetime): Creation date
        company_id (int): ID of the company the user belongs to
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # Index for name searches
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user", index=True)  # Index for role filtering
    is_active = Column(Boolean, default=True, index=True)  # Index for active users
    two_factor_secret = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)  # Index for date filtering
    company_id = Column(Integer, ForeignKey("companies.id"), index=True)  # Index for company filtering
class Client(Base):
    """
    Model that represents a client in the CRM system.

    Clients are associated with a company and can have
    multiple notes, opportunities, and invoices related.

    Attributes:
        id (int): Unique identifier of the client
        name (str): Name of the client
        email (str): Client's email address
        phone (str): Phone number
        company_id (int): ID of the company
        created_by (int): ID of the user who created the client
        created_at (datetime): Creation date
        notes (relationship): Notes associated with the client
        invoices (relationship): Invoices of the client
    """
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # Index for name searches
    email = Column(String, unique=True, index=True)  # Index for email searches
    phone = Column(String)
    company_id = Column(Integer, ForeignKey("companies.id"), index=True)
    created_by = Column(Integer, ForeignKey("users.id"), index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    notes = relationship("Note", backref="client")
    invoices = relationship("Invoice", backref="client")
class Note(Base):
    """
    Model for notes associated with clients.

    Notes allow registering additional information about clients.

    Attributes:
        id (int): Unique identifier of the note
        client_id (int): ID of the associated client
        content (str): Content of the note
        created_at (datetime): Creation date
    """
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class Opportunity(Base):
    """
    Modelo que representa una oportunidad de venta.

    Las oportunidades están asociadas a un cliente y pueden tener
    diferentes etapas en el proceso de venta.

    Attributes:
        id (int): Identificador único de la oportunidad
        name (str): Nombre de la oportunidad
        value (float): Valor monetario de la oportunidad
        stage (str): Etapa actual de la oportunidad
        probability (float): Probabilidad de cierre (0-1)
        client_id (int): ID del cliente asociado
        assigned_user_id (int): ID del usuario asignado
    """
    __tablename__ = "opportunities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    value = Column(Float, index=True)  # Index for value filtering
    stage = Column(String, index=True)  # Index for stage filtering
    probability = Column(Float)
    client_id = Column(Integer, ForeignKey("clients.id"), index=True)
    assigned_user_id = Column(Integer, ForeignKey("users.id"), index=True)

class Task(Base):
    """
    Modelo que representa una tarea en el sistema.

    Las tareas pueden estar relacionadas con clientes u oportunidades
    y tienen diferentes estados de progreso.

    Attributes:
        id (int): Identificador único de la tarea
        title (str): Título de la tarea
        description (str): Descripción detallada
        due_date (datetime): Fecha límite
        priority (str): Prioridad de la tarea (low, medium, high)
        status (str): Estado (pending, in_progress, completed, cancelled)
        assigned_user_id (int): ID del usuario asignado
        created_by (int): ID del usuario que creó la tarea
        related_client_id (int): ID del cliente relacionado (opcional)
        related_opportunity_id (int): ID de la oportunidad relacionada (opcional)
        created_at (datetime): Fecha de creación
        updated_at (datetime): Fecha de última actualización
    """
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    due_date = Column(DateTime, index=True)  # Index for due date filtering
    priority = Column(String, default="medium", index=True)  # Index for priority filtering
    status = Column(String, default="pending", index=True)  # Index for status filtering
    assigned_user_id = Column(Integer, ForeignKey("users.id"), index=True)
    created_by = Column(Integer, ForeignKey("users.id"), index=True)
    related_client_id = Column(Integer, ForeignKey("clients.id"), nullable=True, index=True)
    related_opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
class Invoice(Base):
    """
    Modelo que representa una factura en el sistema.

    Las facturas están asociadas a clientes y pueden tener
    diferentes estados de pago.

    Attributes:
        id (int): Identificador único de la factura
        client_id (int): ID del cliente facturado
        amount (float): Monto de la factura
        status (str): Estado de la factura
        created_at (datetime): Fecha de creación
        due_date (datetime): Fecha de vencimiento
        paypal_payment_id (str): ID de pago de PayPal (opcional)
    """
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), index=True)
    amount = Column(Float, index=True)  # Index for amount filtering
    status = Column(String, default="pending", index=True)  # Index for status filtering
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    due_date = Column(DateTime, index=True)  # Index for due date filtering
    paypal_payment_id = Column(String, nullable=True)

class LogAuditoria(Base):
    """
    Modelo para registro de auditoría del sistema.

    Registra todas las acciones importantes realizadas por los usuarios.

    Attributes:
        id (int): Identificador único del log
        usuario (str): Nombre del usuario que realizó la acción
        accion (str): Descripción de la acción realizada
        fecha (datetime): Fecha y hora de la acción
    """
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    usuario = Column(String, index=True)
    accion = Column(String, index=True)
    fecha = Column(DateTime, default=datetime.utcnow, index=True)

class Points(Base):
    """
    Modelo para el sistema de puntos de gamificación.

    Los usuarios acumulan puntos por diferentes acciones en el sistema.

    Attributes:
        id (int): Identificador único del registro de puntos
        user_id (int): ID del usuario
        points (int): Cantidad de puntos
        reason (str): Razón por la que se otorgaron los puntos
        created_at (datetime): Fecha de creación
    """
    __tablename__ = "points"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    points = Column(Integer, default=0, index=True)
    reason = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class Achievement(Base):
    """
    Modelo que representa un logro en el sistema de gamificación.

    Los logros son metas que los usuarios pueden desbloquear.

    Attributes:
        id (int): Identificador único del logro
        name (str): Nombre del logro
        description (str): Descripción del logro
        points_required (int): Puntos requeridos para desbloquear
        badge_icon (str): Icono del badge (emoji)
    """
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    description = Column(String)
    points_required = Column(Integer, index=True)
    badge_icon = Column(String)

class UserAchievement(Base):
    """
    Modelo que registra los logros desbloqueados por usuarios.

    Relación muchos a muchos entre usuarios y logros.

    Attributes:
        id (int): Identificador único del registro
        user_id (int): ID del usuario
        achievement_id (int): ID del logro desbloqueado
        unlocked_at (datetime): Fecha de desbloqueo
    """
    __tablename__ = "user_achievements"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), index=True)
    unlocked_at = Column(DateTime, default=datetime.utcnow, index=True)

class Notification(Base):
    """
    Modelo que representa una notificación en el sistema.

    Las notificaciones pueden estar relacionadas con tareas,
    clientes u oportunidades específicas.

    Attributes:
        id (int): Identificador único de la notificación
        title (str): Título de la notificación
        message (str): Contenido del mensaje
        type (str): Tipo de notificación (info, warning, success, error)
        is_read (bool): Indica si la notificación fue leída
        user_id (int): ID del usuario destinatario
        related_task_id (int): ID de tarea relacionada (opcional)
        related_client_id (int): ID de cliente relacionado (opcional)
        related_opportunity_id (int): ID de oportunidad relacionada (opcional)
        created_at (datetime): Fecha de creación
        updated_at (datetime): Fecha de última actualización
    """
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    message = Column(Text)
    type = Column(String, default="info", index=True)  # Index for type filtering
    is_read = Column(Boolean, default=False, index=True)  # Index for read status
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    related_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True, index=True)
    related_client_id = Column(Integer, ForeignKey("clients.id"), nullable=True, index=True)
    related_opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
