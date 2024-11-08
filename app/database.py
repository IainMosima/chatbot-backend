from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

async def connect_to_db():
    client = AsyncIOMotorClient(MONGO_URI)
    return client

async def get_db():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[os.getenv("DATABASE_NAME")]
    try:
        yield db
    finally:
        client.close()