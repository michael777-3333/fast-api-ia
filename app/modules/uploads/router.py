from fastapi import APIRouter, UploadFile, File,Form
from .controller import upload_file,save_new_file,get_uploads_id
from typing import List

router = APIRouter(prefix="/uploads", tags=["Uploads"])
@router.get("")
async def get_uploads():
    return await upload_file()

@router.post("")
async def post_uploads( files: List[UploadFile] = File(...),user_id: str = Form(...)):
    return await save_new_file(files,user_id)

@router.get("/{upload_id}")
async def get_uploads(upload_id: str):
    print(upload_id)
    return await get_uploads_id(upload_id)