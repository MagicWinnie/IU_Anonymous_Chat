from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models import Message


async def initialize_database():
    client = AsyncIOMotorClient()
    await init_beanie(
        database=client.ChatService,
        document_models=[
            Message
        ]
    )