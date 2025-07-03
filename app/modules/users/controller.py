
from .service import create_user,ask_ia
from .entity import AskRequest
async def new_user(user_data: dict):
    return await create_user(user_data)

async def new_question(ask_data:AskRequest):
    return await ask_ia(ask_data)