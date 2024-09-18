from datetime import datetime

from pydantic import BaseModel


class Message(BaseModel):
    message: str
    time: datetime
