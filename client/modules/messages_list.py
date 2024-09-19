import flet as ft

from modules.api import API
from modules.message_row import ChatMessage


class MessagesList(ft.Container):
    def __init__(self, api: API, *args, **kwargs):
        self.chat = ft.ListView(expand=True, spacing=10, auto_scroll=True)
        super().__init__(*args, **kwargs, content=self.chat)
        self.api = api
        self.running = False
        self.last_message_id = -1

    def did_mount(self):
        self.running = True
        self.page.run_thread(self.fetch_messages)

    def will_unmount(self):
        self.running = False

    def fetch_messages(self):
        while self.running:
            if not self.api.base_url:
                continue
            messages = self.api.messages(self.last_message_id)
            if messages is None:
                continue  # TODO: fix
            for message in messages:
                self.chat.controls.append(ChatMessage(message))
                self.last_message_id = message.message_id
            self.update()
