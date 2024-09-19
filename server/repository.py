from models import Message

from datetime import datetime
from datetime import timezone

class MessageRepository:
    @staticmethod
    async def create_message(text: str):
        last_message = await Message.find().sort(-Message.message_id).first_or_none()

        if last_message is None:
            new_message_id = 0
        else:
            new_message_id = last_message.message_id + 1

        await Message(message_id=new_message_id, text=text, date_time=datetime.now(timezone.utc)).insert()

    @staticmethod
    async def count_messages():
        return await Message.find().count()
    
    @staticmethod
    async def get_new_messages(offset_message_id: int = -1):
        return await Message.find(Message.message_id > offset_message_id).to_list()
