from typing import Optional

from pydantic import BaseModel


class CreateTopic(BaseModel):
    userId: str
    prompt: str
    chat_history: list[str]
    topicId: Optional[str]

class LLMResponse(BaseModel):
    answer: str
    chat_history: list[str]
    topic: Optional[str]

class FinalResponse(LLMResponse):
    userId: str
