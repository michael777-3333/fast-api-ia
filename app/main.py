from fastapi import FastAPI
from app.routers import api_router
from app.db.mongo import mongo
import os
from dotenv import load_dotenv
import motor.motor_asyncio
from contextlib import asynccontextmanager

load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")

@asynccontextmanager
async def lifespan(app: FastAPI):
    #  Al iniciar FastAPI
    mongo.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    mongo.db = mongo.client[DB_NAME]
    print("✅ Conectado a MongoDB")

    yield  #  Aquí arranca el servidor

    #  Al apagar FastAPI
    mongo.client.close()
    print("🛑 Desconectado de MongoDB")

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)