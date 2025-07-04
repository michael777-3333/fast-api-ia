
from .service import create_user,ask_ia,get_all_uploads
from .entity import AskRequest,Get_uploads
async def new_user(user_data: dict):
    return await create_user(user_data)

async def new_question(ask_data:AskRequest):
    return await ask_ia(ask_data)

async def get_upload_file(req:Get_uploads):
    return await get_all_uploads(req)