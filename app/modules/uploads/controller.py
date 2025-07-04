from fastapi import UploadFile, File,Form
from .service import save_file,get_upload_by_id
from typing import List

async def upload_file():
    return {"filename"}


async def save_new_file(files: List[UploadFile] = File(...), user_id: str = Form(...)):
    for file in files:
        file_path = await save_file(file,user_id)
    return file_path

async def get_uploads_id(upload_id: str):
    return await get_upload_by_id(upload_id)