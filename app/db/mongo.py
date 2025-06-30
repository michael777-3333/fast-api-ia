import motor.motor_asyncio
from typing import Optional

class Mongo:
    client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None
    db = None

mongo = Mongo()