from fastapi import UploadFile, File,Form
from .service import save_file

async def upload_file():
    return {"filename"}


async def save_new_file(file: UploadFile = File(...), user_id: str = Form(...)):
    file_path = await save_file(file,user_id)
    return {"filename": file.filename, "saved_to": file_path}