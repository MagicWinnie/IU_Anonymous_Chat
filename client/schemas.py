from datetime import datetime

from pydantic import BaseModel, Field


class Message(BaseModel):
    text: str
    time: datetime = Field(default_factory=datetime.now)
