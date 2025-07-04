from .entity import User,UserCreate,AskRequest,Get_uploads
from ...modules.uploads.entity import Upload
from app.db.mongo import mongo
from ...gemini.connect_ia import ask_question
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

async def create_user(user_data: UserCreate)->User:
    user = User(**user_data.dict())  # genera id, created_at, etc. Convierte ese modelo Pydantic en un diccionario nativo de Python:
    await mongo.db.users.insert_one(user.dict())
    return user

async def ask_ia(req: AskRequest):
    ansawer =  await ask_question(req.user_id, req.question, req.doc_ids,5)
    return ansawer

async def get_all_uploads(req:Get_uploads):
    cursor = mongo.db.uploads.find({"user_id": req.user_id})
    uploads = await cursor.to_list(length=None)
    # print(uploads)
    cleaned_uploads = convert_objectid(uploads)
    return jsonable_encoder(cleaned_uploads)

def convert_objectid(document):
    if isinstance(document, list):  #La función isinstance() es una función incorporada de Python que se usa para verificar el tipo de una variable u objeto.
        return [convert_objectid(d) for d in document]
    if isinstance(document, dict):
        return {
            key: str(value) if isinstance(value, ObjectId) else convert_objectid(value)
            for key, value in document.items()
        }
    else:
        return document