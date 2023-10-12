from __future__ import annotations
from typing import TYPE_CHECKING

from src.connectors.domain.connector import ConnectorResponse
from src.modules.domain.statusenum import ModuleStatus

if TYPE_CHECKING:
    from src.modules.domain.module import Module
from typing import Any


class ModuleContext:

    def __init__(self, msg: str, user_id, username, module: Module):
        self._msg = msg
        self._user_id = user_id
        self._username = username
        self._module = module
        self._status = ModuleStatus.WAITING
        self._response = None

    def get_msg(self) -> str:
        return self._msg

    def set_msg(self, msg: str):
        self._msg = msg

    def get_username(self):
        return self._username

    def get_user_id(self):
        return self._user_id

    def get_module(self) -> Module:
        return self._module

    def get_status(self) -> ModuleStatus:
        return self._status

    def set_status(self, new_status: ModuleStatus):
        self._status = new_status

    def get_response(self) -> Any[ConnectorResponse]:
        return self._response

    def set_response(self, new_response: ConnectorResponse):
        self._response = new_response
