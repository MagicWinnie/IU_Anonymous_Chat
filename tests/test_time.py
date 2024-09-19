import asyncio
import time

import aiohttp
import numpy as np

from tests.helper import *


async def send_and_receive_messages(send_url, receive_url, num_users):
    async with aiohttp.ClientSession() as session:

        send_tasks = []

        for user_id in range(1, num_users + 1):
            send_tasks.append(send_message(session, send_url, str(user_id)))

        send_start_time = time.time()
        send_responses = await asyncio.gather(*send_tasks)

        send_times = [resp[0] for resp in send_responses if resp[1] == 200]
        send_time = time.time() - send_start_time

        if all(status[1] == 200 for status in send_responses):
            print(f"All messages sent successfully in {send_time:.4f} seconds")
        else:
            print("Some messages failed to send")

        receive_start_time = time.time()

        received_messages = []
        while len(received_messages) < num_users:
            received_messages.append(await receive_messages(session, receive_url, -1))

        receive_time = time.time() - receive_start_time

        print()
        print(f"Received {len(received_messages)} messages in {receive_time:.4f} seconds")
        print(f"Total time for sending and receiving messages: {send_time + receive_time:.4f} seconds")

        send_mean = np.mean(send_times)
        send_std = np.std(send_times)
        send_min = np.min(send_times)
        send_max = np.max(send_times)

        print()
        print(f"Send times - Mean: {send_mean:.4f}, Std: {send_std:.4f}, Min: {send_min:.4f}, Max: {send_max:.4f}")
        print(f"Receive time - {receive_time}")


base_url = "http://127.0.01:8000"
send_url = base_url + "/message/send"
receive_url = base_url + "/messages"
N = 100

asyncio.run(send_and_receive_messages(send_url, receive_url, N))
