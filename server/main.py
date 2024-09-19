import asyncio
import uvicorn

from fastapi import FastAPI, HTTPException

from datetime import datetime

from contextlib import asynccontextmanager

from repository import MessageRepository
from settings import initialize_database, is_mongodb_online
from models import Message


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_database()
    asyncio.create_task(process_queue())
    yield


app = FastAPI(lifespan=lifespan)

message_queue = []

@app.get("/messages/count")
async def count_message():
    return await MessageRepository.count_messages()


@app.post("/message/send")
async def send_message(text: str):
    # Check if repository is online
    if not await is_mongodb_online():
        message_queue.append(text)
        raise HTTPException(status_code=503, detail="MongoDB is offline. Message added to queue.")
    await MessageRepository.create_message(text)

@app.post("/messages/clear")
async def clear_messages():
    await MessageRepository.clear_messages()


@app.get("/messages", response_model=list[Message])
async def get_messages(offset_message_id: int = -1):
    start_time = datetime.now()

    while (datetime.now() - start_time).seconds < 30:
        new_msgs = await MessageRepository.get_new_messages(offset_message_id)
        if new_msgs:
            return new_msgs
        
        await asyncio.sleep(0.5)

    return []


async def process_queue():
    while True:
        if message_queue and await is_mongodb_online():
            while message_queue:
                text = message_queue.pop(0)
                await MessageRepository.create_message(text)
        await asyncio.sleep(3)



if __name__ == "__main__":
    uvicorn.run(app)