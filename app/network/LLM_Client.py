import asyncio
from concurrent.futures import ThreadPoolExecutor
from pydoc_data.topics import topics

from fastapi.params import Depends

from app.database import get_db
from app.network.HTTP_Client import HttpClient
import os
from dotenv import load_dotenv

from app.schemas import LLMResponse, CreateTopic, FinalResponse

load_dotenv()

llm_url = os.getenv("LLM_URL")


class LLMClient:
    def __init__(self):
        self.http_client = HttpClient(
            base_url=llm_url,
            timeout=30,
            retry_attempts=3
        )
        self.executor = ThreadPoolExecutor(max_workers=2)

    async def _fetch_user_topics(self, userId: str, db=Depends(get_db())):
        topics = []

        async for topic in db["topics"].find({"userId": userId}):
            topics.append(topic)
        pass

    async def _concurrent_task(self, topic_data, topic_id):
        llm_result = await asyncio.create_task(self.http_client.post(
            endpoint="/",
            response_model=LLMResponse,
            json=topic_data,
        ))
        user_topics = await asyncio.create_task()

    def chat_with_topic(self, topic_id: str):
        pass


    async def chat_without_topic(self, topic_data:CreateTopic, db):
        llm_result_call = await self.http_client.post(
            endpoint="/get",
            json={"msg": topic_data["prompt"]},
        )
        llm_result = llm_result_call.dict()["data"]
        chat_history = llm_result["chat_history"]




        new_topic = CreateTopic(
            userId=topic_data["userId"],
            prompt=topic_data["prompt"],
            chat_history= chat_history
        ).dict()

        saved_topic = await db["topics"].insert_one(new_topic)

        print("*****Saved Topic*****")
        print(saved_topic)

        result = FinalResponse(
            userId=topic_data["userId"],
            answer=llm_result["answer"],
            chat_history=llm_result["chat_history"],
            topic=llm_result["topic"],
            topicId=str(saved_topic.inserted_id)
        )

        return result
