from fastapi import UploadFile, File
from .service import save_file

async def upload_file():
    return {"filename"}


async def download_file(file: UploadFile = File(...)):
    file_path = await save_file(file)
    return {"filename": file.filename, "saved_to": file_path}