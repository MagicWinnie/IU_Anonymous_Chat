import flet as ft

from message_row import ChatMessage
from schemas import Message
from utils import is_valid_url


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.title = "Anonymous Chat"

    def join_chat_click(e):
        if not ip_address_server.value:
            ip_address_server.error_text = "Server address cannot be blank!"
            ip_address_server.update()
        elif not is_valid_url(ip_address_server.value):
            ip_address_server.error_text = "Server address is invalid!"
            ip_address_server.update()
        else:
            page.close(dig)

    def send_message_click(e):
        if new_message.value != "":
            page.pubsub.send_all(Message(text=new_message.value))
            new_message.value = ""
            new_message.focus()
            page.update()

    def on_message(message: Message):
        chat.controls.append(ChatMessage(message))
        page.update()

    page.pubsub.subscribe(on_message)

    ip_address_server = ft.TextField(
        label="Enter the address of the server",
        autofocus=True,
        on_submit=join_chat_click,
    )

    dig = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([ip_address_server], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(text="Join anonymous chat", on_click=join_chat_click)],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(dig)

    # Chat messages
    chat = ft.ListView(expand=True, spacing=10, auto_scroll=True)

    # A new message entry form
    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    # Add everything to the page
    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(icon=ft.icons.SEND_ROUNDED, tooltip="Send message", on_click=send_message_click),
            ]
        ),
    )


ft.app(target=main)
