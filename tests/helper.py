import time


async def send_message(session, url, message):
    start_time = time.time()
    async with session.post(url, params={"text": message}) as response:
        end_time = time.time()
        return end_time - start_time, response.status, response.reason


async def receive_messages(session, url, offset_message_id):
    start_time = time.time()
    async with session.get(url, params={"offset_message_id": offset_message_id}) as response:
        end_time = time.time()
        return end_time - start_time, await response.json()
