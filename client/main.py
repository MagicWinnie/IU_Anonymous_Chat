import flet as ft

from modules import texts
from modules.api import API
from modules.message_queue import MessageQueue
from modules.messages_list import MessagesList
from modules.utils import is_valid_url


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
    page.title = texts.PAGE_TITLE

    api = API()

    send_message_queue = MessageQueue(api)
    send_message_queue.start()

    def join_chat_click(e):
        if not ip_address_server.value:
            ip_address_server.error_text = texts.SERVER_ADDRESS_EMPTY
            ip_address_server.update()
        elif not is_valid_url(ip_address_server.value):
            ip_address_server.error_text = texts.SERVER_ADDRESS_INVALID
            ip_address_server.update()
        else:
            api.set_base_url(ip_address_server.value)
            if api.messages_count() is None:
                ip_address_server.error_text = texts.SERVER_NOT_RESPONDING
                ip_address_server.update()
                return
            page.close(dig)

    def send_message_click(e):
        if new_message.value:
            send_message_queue.queue.put(new_message.value)
            new_message.value = ""
            new_message.focus()
            page.update()

    ip_address_server = ft.TextField(
        label=texts.SERVER_ADDRESS_INPUT_LABEL,
        autofocus=True,
        on_submit=join_chat_click,
    )

    dig = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text(texts.WELCOME_DIALOG_TITLE),
        content=ft.Column([ip_address_server], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(text=texts.WELCOME_DIALOG_JOIN_BUTTON, on_click=join_chat_click)],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(dig)

    # A new message entry form
    new_message = ft.TextField(
        hint_text=texts.NEW_MESSAGE_INPUT_HINT,
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
        MessagesList(
            api,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip=texts.SEND_MESSAGE_TOOLTIP,
                    on_click=send_message_click
                ),
            ]
        ),
    )


ft.app(target=main)
