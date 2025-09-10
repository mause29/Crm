from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Users
class UserBase(BaseModel):
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    class Config:
        orm_mode = True

# Clients
class ClientBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None

class ClientCreate(ClientBase): pass

class ClientOut(ClientBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

# Opportunities
class OpportunityBase(BaseModel):
    title: str
    stage: str
    estimated_value: float
    probability: float

class OpportunityCreate(OpportunityBase): pass

class OpportunityOut(OpportunityBase):
    id: int
    client_id: int
    class Config:
        orm_mode = True

# Tasks
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to: int
    due_date: datetime

class TaskCreate(TaskBase): pass

class TaskOut(TaskBase):
    id: int
    client_id: int
    completed: bool
    class Config:
        orm_mode = True
