from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.connectors.domain.connector import Connector


class ConnectorContext:

    def __init__(self, msg: str, msg_id, user_id, username, room_id, connector: Connector, session):
        self._msg = msg
        self._msg_id = msg_id
        self._user_id = user_id
        self._username = username
        self._room_id = room_id
        self._connector = connector
        self._session = session

    def get_msg(self):
        return self._msg

    def get_msg_id(self):
        return self._msg_id

    def get_room_id(self):
        return self._room_id

    def get_username(self):
        return self._username

    def get_user_id(self):
        return self._user_id

    def get_connector(self):
        return self._connector

    def get_session(self):
        return self._session
