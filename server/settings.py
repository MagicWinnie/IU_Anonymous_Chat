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

async def is_mongodb_online():
    try:
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        await client.admin.command("ping")
        return True
    except Exception:
        return False