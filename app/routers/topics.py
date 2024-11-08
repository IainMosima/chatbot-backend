from fastapi import APIRouter, Depends

from ..network.LLM_Client import LLMClient
from ..schemas import CreateTopic, LLMResponse
from ..database import get_db
from app.network.HTTP_Client import HttpClient
import os
from dotenv import load_dotenv


router = APIRouter(
    prefix="/topic",
    tags=["topic"],
)

llm_client = LLMClient()

# /topic-titles?userId=1
@router.get("/topic-titles")
async def get_topics(userId: str, db=Depends(get_db)):
    print("User Id", userId)
    topics = await db.topics.find({"userId": userId}).to_list(length=100)
    print("******Topis********")
    print(topics)
    return [topic["title"] for topic in topics]

# Todo: Create chatting function
@router.post("/")
async def chat(topic: CreateTopic, db=Depends(get_db)):
    print("*******Topic Data********")
    print(topic)
    topic_data = topic.dict()
    # Invoke llm
    if not topic_data["chat_history"]:
        # ll_result = llm_client.post(
        #     endpoint="/",
        #     response_model=LLMResponse,
        #     json=topic_data,
        # )

        result = await llm_client.chat_without_topic(topic_data, db=db)

        return result

    else:
        # Todo: Work on here immediately
        # fetch chat_history from mongo_db

        pass


    return "Nothing!!!"

# Todo: Function to delete a topic
@router.delete("/{topic_id}")
def delete_topic(topic_id: int, db=Depends(get_db)):
    pass