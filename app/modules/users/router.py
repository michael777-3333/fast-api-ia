from .controller import new_user,new_question,get_upload_file
from fastapi import APIRouter
from .entity import UserOut,UserCreate,AskRequest,Get_uploads
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("",response_model=UserOut)
async def create_user(user_data: UserCreate):
    return await new_user(user_data)

@router.post("/ask")
async def ask(req: AskRequest):
    respuesta = await new_question(req)
    return {"respuesta": respuesta}

@router.get("")
async def get_uploads(req:Get_uploads):
    print(req)
    return await get_upload_file(req)