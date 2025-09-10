from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    """
    Modelo para crear un nuevo usuario.

    Requiere nombre, email y contraseña válidos.
    La contraseña debe tener al menos 8 caracteres con mayúsculas, minúsculas y dígitos.
    """
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre completo del usuario",
        examples=["Juan Pérez"]
    )
    email: EmailStr = Field(
        ...,
        description="Correo electrónico único del usuario",
        examples=["juan.perez@empresa.com"]
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Contraseña segura (mínimo 8 caracteres, con mayúsculas, minúsculas y dígitos)",
        examples=["SecurePass123"]
    )
    role: str = Field(
        default="user",
        pattern=r"^(user|admin|manager)$",
        description="Rol del usuario en el sistema",
        examples=["user"]
    )
    company_id: Optional[int] = Field(
        None,
        description="ID de la compañía (opcional para usuarios independientes)",
        examples=[1]
    )

    @field_validator('password')
    @classmethod
    def password_strength(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        return v

class UserLogin(BaseModel):
    """
    Modelo para iniciar sesión de usuario.

    Utiliza el email como username.
    """
    username: EmailStr = Field(
        ...,
        description="Correo electrónico del usuario",
        examples=["juan.perez@empresa.com"]
    )
    password: str = Field(
        ...,
        description="Contraseña del usuario",
        examples=["SecurePass123"]
    )

class ClientCreate(BaseModel):
    """
    Modelo para crear un nuevo cliente.

    Información básica de contacto del cliente.
    """
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre completo del cliente",
        examples=["María García"]
    )
    email: EmailStr = Field(
        ...,
        description="Correo electrónico del cliente",
        examples=["maria.garcia@cliente.com"]
    )
    phone: str = Field(
        ...,
        pattern=r'^\+?[\d\s\-\(\)]+$',
        description="Número de teléfono del cliente",
        examples=["+34 612 345 678"]
    )

class OpportunityCreate(BaseModel):
    """
    Modelo para crear una nueva oportunidad de venta.

    Representa una oportunidad comercial con un cliente.
    """
    name: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Nombre descriptivo de la oportunidad",
        examples=["Proyecto Desarrollo Web"]
    )
    value: float = Field(
        ...,
        gt=0,
        description="Valor monetario de la oportunidad",
        examples=[15000.50]
    )
    client_id: int = Field(
        ...,
        gt=0,
        description="ID del cliente asociado",
        examples=[1]
    )

class InvoiceCreate(BaseModel):
    """
    Modelo para crear una nueva factura.

    Información básica de la factura a generar.
    """
    client_id: int = Field(
        ...,
        gt=0,
        description="ID del cliente facturado",
        examples=[1]
    )
    amount: float = Field(
        ...,
        gt=0,
        description="Monto total de la factura",
        examples=[2500.75]
    )
    due_date: Optional[str] = Field(
        None,
        description="Fecha de vencimiento (formato YYYY-MM-DD)",
        examples=["2024-12-31"]
    )

class NotificationCreate(BaseModel):
    """
    Modelo para crear una nueva notificación.

    Mensaje para enviar a un usuario específico.
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Título de la notificación",
        examples=["Nueva tarea asignada"]
    )
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Contenido del mensaje de notificación",
        examples=["Se te ha asignado una nueva tarea: Revisar propuesta comercial"]
    )
    type: str = Field(
        default="info",
        pattern=r"^(info|warning|success|error)$",
        description="Tipo de notificación",
        examples=["info"]
    )
    user_id: int = Field(
        ...,
        gt=0,
        description="ID del usuario destinatario",
        examples=[1]
    )
