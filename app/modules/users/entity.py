from pydantic import BaseModel, Field,EmailStr
from typing import Optional
from datetime import datetime
import uuid

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# DTO de salida (lo que devuelves al cliente)
class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: datetime

# Entidad principal (incluye UUID, timestamps, etc.)
class User(UserCreate):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


class AskRequest(BaseModel):
    user_id: str
    doc_ids: list[str] | None = None
    question: str

class Get_uploads(BaseModel):
    user_id: str