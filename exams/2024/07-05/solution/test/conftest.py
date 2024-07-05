import pytest  # noqa: F401
import requests
from config import base_url
from funcy import project
from utils import Struct


def pytest_configure():
    pytest.data = {"admin": {}, "alexcarrega": {}}


@pytest.fixture()
def auth_request(username: str, password: str):
    response = requests.post(
        f"{base_url}/auth/token",
        data=dict(username=username, password=password),
    )
    return Struct(
        **project(response.json(), ["access_token", "refresh_token"])
    )


@pytest.fixture()
def auth_header(auth_request):
    return {"Authorization": f"Bearer {auth_request.access_token}"}
