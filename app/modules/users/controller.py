
from .service import create_user

async def new_user(user_data: dict):
    return await create_user(user_data)