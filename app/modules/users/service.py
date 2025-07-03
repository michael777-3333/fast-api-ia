from .entity import User,UserCreate,AskRequest
from app.db.mongo import mongo
from ...gemini.connect_ia import ask_question


async def create_user(user_data: UserCreate)->User:
    user = User(**user_data.dict())  # genera id, created_at, etc. Convierte ese modelo Pydantic en un diccionario nativo de Python:
    await mongo.db.users.insert_one(user.dict())
    return user

async def ask_ia(req: AskRequest):
    ansawer =  await ask_question(req.user_id, req.question, req.doc_ids,5)
    return ansawer
