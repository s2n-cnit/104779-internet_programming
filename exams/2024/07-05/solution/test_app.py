import json
import os
from enum import Enum
from typing import Self

import pytest
from app import app
from db import Action
from fastapi import status
from fastapi.testclient import TestClient
from jinja2 import Template

client = TestClient(app)

field_check = dict(tag="name", category="name", command="path")


class CommandTagAction(str, Enum):
    ADD_TAG = "add-tag"
    RM_TAG = "rm-tag"


class CommandTagGoal(str, Enum):
    OK = "Ok"
    COMMAND_NOT_FOUND = "Command not found",
    TAG_NOT_FOUND = "Tag not found"
    COMMAND_TAG_FOUND = "Command - Tag found"
    COMMAND_TAG_NOT_FOUND = "Command - Tag not found"


@pytest.mark.parametrize(
    "username,password", [("admin", "admin"), ("alexcarrega", "test-me")]
)
@pytest.mark.parametrize("role", ["admin", "me"])
@pytest.mark.parametrize("target", ["category", "tag", "workflow", "command"])
class TestAPP:

    def init(self: Self, kwrd_args: dict) -> None:
        for k, v in kwrd_args.items():
            self.__setattr__(k, v)

    def has_path(self: Self) -> bool:
        self.path = f"test_data/{self.target}/{self.action}.json"
        return os.path.exists(self.path)

    def get_data(self: Self, **params: dict) -> dict:
        _buffer = open(self.path).read()
        print(params)
        _tpl = Template(_buffer)
        _txt = _tpl.render(**params)
        return json.loads(_txt)

    def get_id(self: Self) -> str | int:
        if "-NF" in self.action:
            return 0
        else:
            return pytest.data[self.username][self.target]

    def get_url(self: Self, end: str = "") -> str:
        return f"/{self.role}/{self.target}{end}"

    def is_action_ok(self: Self) -> bool:
        return ("-NF" not in self.action and "-NC" not in self.action and
                self.status_code == status.HTTP_200_OK)

    def check_auth(self: Self) -> bool:
        if self.role == "admin" and self.username != "admin":
            assert self.response.status_code == status.HTTP_401_UNAUTHORIZED
            return False
        return True

    def check_data(self: Self, single: bool) -> None:
        if self.is_action_ok():
            _data = self.response.json()
            if single:
                assert type(_data) is dict
                assert field_check[self.target] in _data
                if self.role != "admin":
                    assert _data["created_by_id"] == self.username
                    assert _data["updated_by_id"] in [self.username, None]
            else:
                assert type(_data) is list
                assert len(_data) > 0
                found = False
                for item in _data:
                    if item["id"] == pytest.data[self.username][self.target]:
                        found = True
                        break
                assert found
                if self.role != "admin":
                    for _itm in _data:
                        assert _itm["created_by_id"] == self.username
                        assert _itm["updated_by_id"] in [self.username, None]

    def check_result(self: Self, output: str) -> None:
        if self.is_action_ok():
            _data = self.response.json()
            assert _data["action"] == output
            pytest.data[self.username][self.target] = _data["id"]

    def make_response(
        self: Self,
        method: callable,
        url: str,
        with_data: bool,
        params: dict = {},
    ):
        if not self.has_path():
            return False
        self.response = method(
            url,
            headers=self.auth_header,
            json=self.get_data(**params) if with_data else None,
        )
        if self.check_auth():
            assert self.response.status_code == self.status_code
            assert self.response.headers["Content-Type"] == "application/json"
            return True
        else:
            return False

    @pytest.mark.parametrize(
        "action,status_code",
        [
            ("create", status.HTTP_200_OK),
            ("create-NC", status.HTTP_422_UNPROCESSABLE_ENTITY),
            ("create-workflow-NF", status.HTTP_404_NOT_FOUND),
            ("create-category-NF", status.HTTP_404_NOT_FOUND),
            ("create-workflow-category-NF", status.HTTP_404_NOT_FOUND),
            ("create-NC-category-NF", status.HTTP_422_UNPROCESSABLE_ENTITY),
            ("create-NC-workflow-NF", status.HTTP_422_UNPROCESSABLE_ENTITY),
            (
                "create-NC-workflow-category-NF",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            ),
        ],
    )
    @pytest.mark.order(1)
    def test_create(
        self: Self,
        username: str,
        auth_header: str,  # noqa: F811
        role: str,
        target: str,
        action: str,
        status_code: int,
    ) -> None:
        if target == "command":
            assert "category" in pytest.data[username]
            assert "workflow" in pytest.data[username]
            params = dict(
                workflow_id=pytest.data[username]["workflow"],
                category_id=pytest.data[username]["category"],
            )
        else:
            params = {}
        self.init(locals())
        _url = self.get_url()
        if self.make_response(client.post,
                              url=_url,
                              with_data=True,
                              params=params):
            self.check_result("Created")

    @pytest.mark.parametrize(
        "action,status_code",
        [
            ("read", status.HTTP_200_OK),
            ("read-NF", status.HTTP_404_NOT_FOUND),
        ],
    )
    @pytest.mark.order(2)
    def test_read(
        self: Self,
        username: str,
        auth_header: str,  # noqa: F811
        role: str,
        target: str,
        action: str,
        status_code: int,
    ) -> None:
        self.init(locals())
        _url = self.get_url(end=f"/{self.get_id()}")
        if self.make_response(client.get, url=_url, with_data=False):
            self.check_data(single=True)

    @pytest.mark.parametrize(
        "action,status_code,part",
        [
            ("read", status.HTTP_200_OK, ""),
            ("created", status.HTTP_200_OK, "/created"),
            ("updated", status.HTTP_200_OK, "/updated"),
        ],
    )
    @pytest.mark.order(4)
    def test_read_all(
        self: Self,
        username: str,
        auth_header: dict,  # noqa: F811
        role: str,
        target: str,
        action: str,
        status_code: int,
        part: str,
    ) -> None:
        if role == "me" and action == "read":
            status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        if role == "admin" and action != "read":
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        self.init(locals())
        _url = self.get_url(end=self.part)
        if self.make_response(client.get, url=_url, with_data=False):
            self.check_data(single=False)

    @pytest.mark.parametrize(
        "action,status_code",
        [
            ("update", status.HTTP_200_OK),
            ("update-category-NF", status.HTTP_404_NOT_FOUND),
            ("update-workflow-NF", status.HTTP_404_NOT_FOUND),
            ("update-NF", status.HTTP_404_NOT_FOUND),
            ("update-NC", status.HTTP_422_UNPROCESSABLE_ENTITY),
            ("update-NC-NF", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ],
    )
    @pytest.mark.order(3)
    def test_update(
        self: Self,
        username: str,
        auth_header: dict,  # noqa: F811
        role: str,
        target: str,
        action: str,
        status_code: int,
    ) -> None:
        if target == "command":
            assert "workflow" in pytest.data[username]
            assert "category" in pytest.data[username]
            params = dict(
                workflow_id=pytest.data[username]["workflow"],
                category_id=pytest.data[username]["category"],
            )
        else:
            params = {}
        self.init(locals())
        _url = self.get_url(end=f"/{self.get_id()}")
        if self.make_response(client.put,
                              url=_url,
                              with_data=True,
                              params=params):
            self.check_result("Updated")

    @pytest.mark.parametrize(
        "action,status_code",
        [
            ("delete", status.HTTP_200_OK),
            ("delete-NF", status.HTTP_404_NOT_FOUND),
        ],
    )
    @pytest.mark.order(5)
    def test_delete(
        self: Self,
        username: str,
        auth_header: dict,  # noqa: F811
        role: str,
        target: str,
        action: str,
        status_code: int,
    ) -> None:
        if role == "me":
            status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        self.init(locals())
        _url = self.get_url(end=f"/{self.get_id()}")
        if self.make_response(client.delete, url=_url, with_data=False):
            self.check_result("Deleted")

    @pytest.mark.parametrize(
        "action,goal,status_code",
        [
            (CommandTagAction.ADD_TAG, CommandTagGoal.OK, status.HTTP_200_OK),
            (
                CommandTagAction.ADD_TAG,
                CommandTagGoal.COMMAND_NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            ),
            (
                CommandTagAction.ADD_TAG,
                CommandTagGoal.TAG_NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            ),
            (
                CommandTagAction.ADD_TAG,
                CommandTagGoal.COMMAND_TAG_FOUND,
                status.HTTP_409_CONFLICT,
            ),
            (CommandTagAction.RM_TAG, CommandTagGoal.OK, status.HTTP_200_OK),
            (
                CommandTagAction.RM_TAG,
                CommandTagGoal.COMMAND_TAG_NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            ),
        ],
    )
    @pytest.mark.order(6)
    def test_manage_tag(
        self: Self,
        username: str,
        auth_header: dict,  # noqa: F811
        role: str,
        target: str,
        action: str,
        goal: str,
        status_code: int,
    ) -> None:
        if target == "command":
            self.init(locals())
            match goal:
                case CommandTagGoal.OK:
                    _id = pytest.data[self.username][self.target]
                    _tag_id = pytest.data[self.username]["tag"]
                case CommandTagGoal.COMMAND_NOT_FOUND:
                    _id = 0
                    _tag_id = pytest.data[self.username]["tag"]
                case CommandTagGoal.TAG_NOT_FOUND:
                    _id = pytest.data[self.username][self.target]
                    _tag_id = 0
                case CommandTagGoal.COMMAND_TAG_NOT_FOUND:
                    _id = pytest.data[self.username][self.target]
                    _tag_id = pytest.data[self.username]["tag"]
            _response = client.put(f"/command/{_id}/{action}/{_tag_id}",
                                   headers=auth_header)
            if self.check_auth():
                assert self.response.status_code == self.status_code
                assert (self.response.headers["Content-Type"] ==
                        "application/json")
                _json = _response.json()
                assert "action" in _json
                assert _json["action"] == self.action

    @pytest.mark.parametrize(
        "execution,action,status_code",
        [
            ("start", Action.STARTED, status.HTTP_200_OK),
            ("stop", Action.STOPPED, status.HTTP_200_OK),
        ],
    )
    @pytest.mark.order(7)
    def test_execution(
        self: Self,
        username: str,
        auth_header: dict,  # noqa: F811
        role: str,
        target: str,
        execution: str,
        action: str,
        status_code: int,
    ) -> None:
        if target == "workflow":
            self.init(locals())
            _id = pytest.data[self.username][self.target]
            _response = client.put(f"/workflow/{_id}/{execution}",
                                   headers=auth_header)
            if self.check_auth():
                assert self.response.status_code == self.status_code
                assert (self.response.headers["Content-Type"] ==
                        "application/json")
                _json = _response.json()
                assert "action" in _json
                assert _json["action"] == self.action
