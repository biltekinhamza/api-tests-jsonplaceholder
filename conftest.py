import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT = 10  # seconds; requests waits forever without a timeout


class ApiClient:
    """Small wrapper so every request uses the same base URL and timeout."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        return self.session.request(method, f"{BASE_URL}{path}", timeout=TIMEOUT, **kwargs)

    def get(self, path: str, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs):
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs):
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs):
        return self.request("DELETE", path, **kwargs)


@pytest.fixture(scope="session")
def api() -> ApiClient:
    return ApiClient()
