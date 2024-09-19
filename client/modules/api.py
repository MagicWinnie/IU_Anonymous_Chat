from urllib.parse import urljoin

import requests

from modules.schemas import Message


class API:
    def __init__(self):
        self.base_url = ""
        self.session = requests.Session()

    def set_base_url(self, base_url: str):
        self.base_url = base_url

    def messages_count(self) -> int | None:
        url = urljoin(self.base_url, "messages/count")
        try:
            response = self.session.get(url=url, timeout=3)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None

    def message_send(self, text: str) -> bool:
        url = urljoin(self.base_url, "message/send")
        params = {"text": text}
        try:
            response = self.session.post(url=url, params=params)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False

    def messages(self, offset_message_id: int = -1) -> list[Message] | None:
        url = urljoin(self.base_url, "messages")
        params = {"offset_message_id": offset_message_id}
        try:
            response = self.session.get(url=url, params=params)
            response.raise_for_status()
            return [Message(**message) for message in response.json()]
        except requests.exceptions.RequestException:
            return None


def main():
    api = API()
    api.set_base_url("http://10.91.49.21:8000/")
    print(api.messages_count())
    print(api.message_send("Sent from client test"))
    print(api.messages())


if __name__ == '__main__':
    main()
