import asyncio

import aiohttp
import numpy as np
from tqdm.asyncio import tqdm

from tests.helper import *


async def send_and_receive_messages(send_url, receive_url, num_users):
    async with aiohttp.ClientSession() as session:

        send_tasks = []

        for user_id in range(1, num_users + 1):
            send_tasks.append(send_message(session, send_url, str(user_id)))

        send_start_time = time.time()

        # Add a loading bar here
        print(f"Sending {num_users} messages simultaneously...")
        send_responses = await tqdm.gather(*send_tasks, desc="Sending messages", unit="message")

        send_times = [resp[0] for resp in send_responses if resp[1] == 200]
        send_time = time.time() - send_start_time

        if all(status[1] == 200 for status in send_responses):
            print(f"All {num_users} messages sent successfully in \033[1m{send_time:.4f}\033[0m seconds")
        else:
            print("Some messages failed to send")

        receive_start_time = time.time()

        received_messages = []
        while len(received_messages) < num_users:
            received_messages.append(await receive_messages(session, receive_url, -1))

        receive_time = time.time() - receive_start_time

        print()
        print(f"Received {len(received_messages)} messages in \033[1m{receive_time:.4f}\033[0m seconds")
        print(f"Total time for sending and receiving messages: \033[1m{send_time + receive_time:.4f}\033[0m seconds")

        send_mean = np.mean(send_times)
        send_std = np.std(send_times)
        send_min = np.min(send_times)
        send_max = np.max(send_times)

        print()
        print(
            f"Send times - Mean: \033[1m{send_mean:.4f}\033[0m, Std: \033[1m{send_std:.4f}\033[0m, Min: \033[1m{send_min:.4f}\033[0m, Max: \033[1m{send_max:.4f}\033[0m")
        print(f"Receive time - \033[1m{receive_time}\033[0m")


base_url = "http://127.0.01:8000"
send_url = base_url + "/message/send"
receive_url = base_url + "/messages"
N = 100

asyncio.run(send_and_receive_messages(send_url, receive_url, N))
