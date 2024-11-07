from pydantic import BaseModel
from typing import Optional

class Topic(BaseModel):
    userId: Optional[str]
    prompt: str
