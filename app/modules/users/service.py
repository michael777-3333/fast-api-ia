from .entity import User,UserCreate
from app.db.mongo import mongo

async def create_user(user_data: UserCreate)->User:
    user = User(**user_data.dict())  # genera id, created_at, etc. Convierte ese modelo Pydantic en un diccionario nativo de Python:
    await mongo.db.users.insert_one(user.dict())
    return user