from fastapi import APIRouter, UploadFile, File
from .controller import upload_file,download_file
router = APIRouter(prefix="/uploads", tags=["Uploads"])
@router.get("")
async def get_uploads():
    return await upload_file()

@router.post("")
async def post_uploads(file: UploadFile = File(...)):
    return await download_file(file)