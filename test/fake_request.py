class FakeClient:
    def __init__(self, host="127.0.0.1"):
        self.host = host


class FakeURL:
    def __init__(self, path):
        self.path = path


class FakeRequest:
    def __init__(
        self,
        method: str,
        path: str,
        headers: dict | None = None,
        client_ip: str = "127.0.0.1",
    ):
        self.method = method
        self.url = FakeURL(path)
        self.headers = headers or {}
        self.client = FakeClient(client_ip)
