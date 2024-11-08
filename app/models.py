from pydantic import BaseModel
from typing_extensions import Optional, List

class Topic(BaseModel):
    topicId: Optional[str]
    userId: str
    prompt: str
    chat_history: List[str]


