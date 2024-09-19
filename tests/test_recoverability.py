import subprocess
import asyncio
import uuid

import aiohttp
import time
from tests.helper import *



def pause_docker_container(container_name):
    try:
        result = subprocess.run(['docker', 'pause', container_name], check=True, capture_output=True, text=True)
        print(f"{container_name} paused successfully.")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop container {container_name}. Error: {e.stderr}")
        return None


def unpause_docker_container(container_name):
    try:
        result = subprocess.run(['docker', 'unpause', container_name], check=True, capture_output=True, text=True)
        print(f"{container_name} started successfully.")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Failed to start container {container_name}. Error: {e.stderr}")
        return None


async def test_recoverability():
    pause_docker_container('mongodb')


    async with aiohttp.ClientSession() as session:
        send_url = "http://127.0.0.1:8000/message/send"

        # Attempt to send a message while the database is offline
        print("Sending message...")
        # Generate UUID for the message
        message_text = str(uuid.uuid4())
        status = await send_message(session, send_url, message_text)
        print(f"Message send status while DB is offline: {status[1:]}")

        # Start the MongoDB container
        unpause_docker_container('mongodb')

        receive_url = "http://127.0.0.1:8000/messages"
        start_time = time.time()
        while True:
            # Take only first item from each list from list of lists
            messages = (await receive_messages(session, receive_url, -1))[1]

            for message in messages:
                if (message['text'] == message_text):
                    end_time = time.time()
                    print("Test passed")
                    print(f"Time taken for message to be sent: {end_time - start_time:.4f} seconds")
                    exit(0)

        print("Test failed")
        exit(1)


asyncio.run(test_recoverability())