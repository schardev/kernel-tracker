import json
from urllib.request import Request, urlopen


class TelegramUtils:
    def __init__(self, API: str) -> None:
        self.API = API
        self.API_URL = f"https://api.telegram.org/bot{self.API}/sendMessage"
        self.url_data = {}

    def send_to_tg(self, chat_id: str, kvd: dict) -> str:
        """Sends a nicely formatted notification to given Telegram chat_id"""
        self.url_data["chat_id"] = chat_id
        self.url_data["parse_mode"] = "Markdown"

        for rel in kvd:
            for ver in kvd[rel]:
                self.url_data["reply_markup"] = {"inline_keyboard": []}
                message = f"""\
                *New kernel release detected!*\

                \nrelease: `{rel}`\
                \nversion: `{ver}`\
                \ndate: `{kvd[rel][ver]['date']}`
                """
                for i in kvd[rel][ver]:
                    if i == "date":
                        continue
                    self.url_data["reply_markup"]["inline_keyboard"].append(
                        [{"text": f"{i}", "url": f"{kvd[rel][ver][i]}"}]
                    )

                self.url_data["text"] = message
                self._make_send_request()

    def _make_send_request(self):
        req = Request(self.API_URL, data=json.dumps(self.url_data).encode())
        req.add_header("Content-Type", "application/json")
        with urlopen(req) as fp:
            status = fp.read()
