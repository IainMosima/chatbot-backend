from pydantic import BaseModel
from typing_extensions import Optional

class Topic(BaseModel):
    topicId: Optional[str]
    userId: str
    prompt: str
