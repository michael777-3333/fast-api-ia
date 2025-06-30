from fastapi import APIRouter
from .controller import upload_file
router = APIRouter(prefix="/uploads", tags=["Uploads"])
@router.get("")
async def get_uploads():
    return await upload_file()