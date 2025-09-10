from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database_new import Base

class Company(Base):
    """
    Modelo que representa una compañía en el sistema CRM.

    Una compañía puede tener múltiples usuarios y clientes asociados.
    Se utiliza para segmentar datos por empresa en un entorno multi-tenant.

    Attributes:
        id (int): Identificador único de la compañía
        name (str): Nombre de la compañía
        users (relationship): Usuarios pertenecientes a esta compañía
        clients (relationship): Clientes pertenecientes a esta compañía
    """
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    users = relationship("User", backref="company")
    clients = relationship("Client", backref="company")

class User(Base):
    """
    Modelo que representa un usuario del sistema CRM.

    Los usuarios pueden tener diferentes roles (user, admin, manager) y
    pertenecen a una compañía específica.

    Attributes:
        id (int): Identificador único del usuario
        name (str): Nombre completo del usuario
        email (str): Correo electrónico único
        hashed_password (str): Contraseña encriptada
        role (str): Rol del usuario (user, admin, manager)
        is_active (bool): Estado de activación de la cuenta
        two_factor_secret (str): Secreto para autenticación de dos factores
        created_at (datetime): Fecha de creación
        company_id (int): ID de la compañía a la que pertenece
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)
    two_factor_secret = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    company_id = Column(Integer, ForeignKey("companies.id"))

class Client(Base):
    """
    Modelo que representa un cliente en el sistema CRM.

    Los clientes están asociados a una compañía y pueden tener
    múltiples notas, oportunidades e facturas relacionadas.

    Attributes:
        id (int): Identificador único del cliente
        name (str): Nombre del cliente
        email (str): Correo electrónico del cliente
        phone (str): Número de teléfono
        company_id (int): ID de la compañía
        created_by (int): ID del usuario que creó el cliente
        created_at (datetime): Fecha de creación
        notes (relationship): Notas asociadas al cliente
        invoices (relationship): Facturas del cliente
    """
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    company_id = Column(Integer, ForeignKey("companies.id"))
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = relationship("Note", backref="client")
    invoices = relationship("Invoice", backref="client")

class Note(Base):
    """
    Modelo para notas asociadas a clientes.

    Las notas permiten registrar información adicional sobre los clientes.

    Attributes:
        id (int): Identificador único de la nota
        client_id (int): ID del cliente asociado
        content (str): Contenido de la nota
        created_at (datetime): Fecha de creación
    """
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

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
    name = Column(String)
    value = Column(Float)
    stage = Column(String)
    probability = Column(Float)
    client_id = Column(Integer, ForeignKey("clients.id"))
    assigned_user_id = Column(Integer, ForeignKey("users.id"))

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
    title = Column(String)
    description = Column(Text)
    due_date = Column(DateTime)
    status = Column(String, default="pending")  # pending, in_progress, completed, cancelled
    assigned_user_id = Column(Integer, ForeignKey("users.id"))
    created_by = Column(Integer, ForeignKey("users.id"))
    related_client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    related_opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
    client_id = Column(Integer, ForeignKey("clients.id"))
    amount = Column(Float)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
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
    usuario = Column(String)
    accion = Column(String)
    fecha = Column(DateTime, default=datetime.utcnow)

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
    user_id = Column(Integer, ForeignKey("users.id"))
    points = Column(Integer, default=0)
    reason = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

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
    name = Column(String)
    description = Column(String)
    points_required = Column(Integer)
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
    user_id = Column(Integer, ForeignKey("users.id"))
    achievement_id = Column(Integer, ForeignKey("achievements.id"))
    unlocked_at = Column(DateTime, default=datetime.utcnow)

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
    title = Column(String)
    message = Column(Text)
    type = Column(String, default="info")  # info, warning, success, error
    is_read = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    related_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    related_client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    related_opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
