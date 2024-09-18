from datetime import datetime

import flet as ft

from .schemas import Message


class ChatMessage(ft.Row):
    def __init__(self, message: Message, time_text_size: int = 12, msg_text_size: int = 18):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            ft.CircleAvatar(content=ft.Icon(ft.icons.PERSON_ROUNDED)),
            ft.Column(
                [
                    ft.Text(self.get_formatted_time(message.time), italic=True, size=time_text_size),
                    ft.Text(message.text, selectable=True, size=msg_text_size),
                ],
                tight=True,
                spacing=3,
            ),
        ]

    @staticmethod
    def get_formatted_time(time: datetime) -> str:
        return time.strftime("%H:%M:%S %d/%m/%Y")
