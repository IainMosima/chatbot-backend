from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)

db = client[os.getenv("DATABASE_NAME")]

async def connect_to_db():
    await client.wait_until_ready()

async def get_db():
    return db