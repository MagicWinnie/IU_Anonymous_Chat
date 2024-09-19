from beanie import Document
from datetime import datetime


class Message(Document):
    message_id: int
    text: str
    date_time: datetime
    