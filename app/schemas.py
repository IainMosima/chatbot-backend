from pydantic import BaseModel


class CreateTopic(BaseModel):
    userId: str
    prompt: str