import os
import shutil
from fastapi import UploadFile,HTTPException
import fitz  # PyMuPDF
import docx  # Python Docx
import uuid
from datetime import datetime
from .entity import Upload
from app.db.mongo import mongo
from app.gemini.connect_ia import splitter_text,save_data_in_chroma
from bson import ObjectId
from datetime import datetime
TEMP_DIR = "temp_uploads"
ALLOWED_EXTENSIONS = ["pdf", "docx", "txt"]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

async def save_file(file: UploadFile, user_id: str) -> Upload:
    try:
        if not allowed_file(file.filename):
            raise HTTPException(status_code=400, detail="File type not allowed")
        upload = await save_in_db_file(file, user_id)
        os.mkdir(TEMP_DIR)
    except FileExistsError:
        pass
    file_extension = file.filename.split('.')[-1]
    file_path = os.path.join(TEMP_DIR, upload.id + '.' + file_extension)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    upload.extracted_text = extract_text_from_file(file_path)
    await mongo.db.uploads.update_one({"id": upload.id}, {"$set": {"extracted_text": upload.extracted_text}})
    # await invoke('I love programming.')
    chunks=await splitter_text(upload.extracted_text)
    await save_data_in_chroma(upload.user_id, upload.id,chunks)
    return upload
    

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
    file_extension = file.filename.split('.')[-1]
    filename = file.filename
    file_path = os.path.join(TEMP_DIR, filename)
    upload = Upload(
        id=str(uuid.uuid4()),
        user_id=user_id,
        filename=filename,
        content_type=file.content_type,
        storage_url=file_path,
        uploaded_at=datetime.utcnow()
    )
    upload.storage_url=upload.id + '.' + file_extension
    await mongo.db.uploads.insert_one(upload.dict())

    return upload

# async def sliter_text(text:str):
#     print(text)

#     await splitter_text(text)


async def get_upload_by_id(upload_id: str):
    upload = await mongo.db.uploads.find_one({"id": upload_id})
    if not upload:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return serialize_mongo_document(upload)

def serialize_mongo_document(doc: dict) -> dict:
    new_doc = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            new_doc[key] = str(value)
        elif isinstance(value, datetime):
            new_doc[key] = value.isoformat()
        else:
            new_doc[key] = value
    return new_doc