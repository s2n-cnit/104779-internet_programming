import pytest  # noqa: F401
from app import app
from fastapi.testclient import TestClient
from funcy import project

client = TestClient(app)


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def pytest_configure():
    pytest.data = {"admin": {}, "alexcarrega": {}}


@pytest.fixture()
def auth_request(username: str, password: str):
    response = client.post("/auth/token",
                           data=dict(username=username, password=password))
    _tokens = ["access_token", "refresh_token"]
    _json = response.json()
    for token in _tokens:
        assert token in _json
    return Struct(**project(_json, _tokens))


@pytest.fixture()
def auth_header(auth_request):
    return {"Authorization": f"Bearer {auth_request.access_token}"}
