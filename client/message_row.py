import flet as ft

from schemas import Message


class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            ft.CircleAvatar(content=ft.Icon(ft.icons.PERSON_ROUNDED)),
            ft.Column(
                [
                    ft.Text(str(message.time), weight=ft.FontWeight.W_100),
                    ft.Text(message.text, selectable=True),
                ],
                tight=True,
                spacing=5,
            ),
        ]
