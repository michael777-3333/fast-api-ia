from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class UploadCreate(BaseModel):
    user_id: str
    filename: str
    content_type: str

    
class Upload(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str  # Referencia al usuario que lo subió
    filename: str  # Nombre original del archivo
    content_type: str  # MIME type, ej: application/pdf
    storage_url: Optional[str] = None  # URL en S3, GCP o disco local
    extracted_text: Optional[str] = None  # Texto plano procesado
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)