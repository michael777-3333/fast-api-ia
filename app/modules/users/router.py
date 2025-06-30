from .controller import new_user
from fastapi import APIRouter
from .entity import UserOut,UserCreate
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("",response_model=UserOut)
async def create_user(user_data: UserCreate):
    return await new_user(user_data)