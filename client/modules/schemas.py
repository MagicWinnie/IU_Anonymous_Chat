from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class Message(BaseModel):
    message_id: int
    text: str
    date_time: datetime = Field(default_factory=datetime.now)

    def model_post_init(self, __context: Any) -> None:
        if self.date_time.tzinfo is None:
            self.date_time = self.date_time.replace(tzinfo=timezone.utc).astimezone()
