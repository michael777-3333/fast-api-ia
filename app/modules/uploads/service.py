import os
import shutil
from fastapi import UploadFile,HTTPException
import fitz  # PyMuPDF
import docx  # Python Docx
import uuid
from datetime import datetime
from .entity import Upload
from app.db.mongo import mongo
TEMP_DIR = "temp_uploads"
ALLOWED_EXTENSIONS = ["pdf", "docx", "txt"]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

async def save_file(file: UploadFile, user_id: str) -> Upload:
    try:
        if not allowed_file(file.filename):
            raise HTTPException(status_code=400, detail="File type not allowed")
        os.mkdir(TEMP_DIR)
    except FileExistsError:
        pass
    file_path = os.path.join(TEMP_DIR, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return await save_in_db_file(file, user_id)

def extract_text_from_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[-1].lower()
    
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Extensión no soportada: {ext}")
    

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def extract_text_from_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
    

async def save_in_db_file(file: UploadFile, user_id: str):
    filename = file.filename
    file_path = os.path.join(TEMP_DIR, filename)
    upload = Upload(
        id=str(uuid.uuid4()),
        user_id=user_id,
        filename=filename,
        content_type=file.content_type,
        storage_path=file_path,
        uploaded_at=datetime.utcnow()
    )
    await mongo.db.uploads.insert_one(upload.dict())

    return upload