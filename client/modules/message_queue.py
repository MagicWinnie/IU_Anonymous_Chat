from queue import Queue
from threading import Thread

from modules.api import API


class MessageQueue(Thread):
    def __init__(self, api: API):
        Thread.__init__(self)
        self.is_running = True
        self.queue: Queue[str] = Queue()
        self.api = api

    def run(self):
        while self.is_running:
            if not self.api.base_url:
                continue
            text = self.queue.get()
            self.api.message_send(text)
