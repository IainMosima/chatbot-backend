from fastapi import APIRouter, Depends, HTTPException
from ..models import Topic
from ..schemas import CreateTopic
from ..database import get_db


router = APIRouter(
    prefix="/topic",
    tags=["topic"],
)

# /all-topics?userId=1
@router.get("/topic-titles")
async def get_topics(userId, db=Depends(get_db)):
    topics = await db.topics.find({"userId": userId}).to_list(length=100)
    return [topic["title"] for topic in topics]
