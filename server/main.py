import asyncio
import uvicorn

from fastapi import FastAPI

from datetime import datetime

from contextlib import asynccontextmanager

from repository import *
from settings import initialize_database
from models import Message


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_database()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/messages/count")
async def count_message():
    return await MessageRepository.count_messages()


@app.post("/message/send")
async def send_message(text: str):
    await MessageRepository.create_message(text)



@app.get("/messages", response_model=list[Message])
async def get_messages(offset_message_id: int = -1):
    start_time = datetime.now()

    while (datetime.now() - start_time).seconds < 30:
        new_msgs = await MessageRepository.get_new_messages(offset_message_id)
        if new_msgs:
            return new_msgs
        
        await asyncio.sleep(1)

    return {"message": "No new messages"}


if __name__ == "__main__":
    uvicorn.run(app, host="10.91.49.218")