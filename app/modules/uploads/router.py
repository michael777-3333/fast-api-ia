from fastapi import APIRouter, UploadFile, File,Form
from .controller import upload_file,save_new_file
router = APIRouter(prefix="/uploads", tags=["Uploads"])
@router.get("")
async def get_uploads():
    return await upload_file()

@router.post("")
async def post_uploads(file: UploadFile = File(...),user_id: str = Form(...)):
    return await save_new_file(file,user_id)