from fastapi import FastAPI
from .routers import topics
from .database import connect_to_db


app = FastAPI()

app.include_router(topics.router)

@app.on_event("startup")
async def startup():
    await connect_to_db()