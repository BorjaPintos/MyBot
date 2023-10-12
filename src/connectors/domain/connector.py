from abc import abstractmethod
from typing import List, Optional

from src.connectors.domain.connectorcallback import ConnectorCallback
from src.connectors.domain.connectorcontext import ConnectorContext


class ConnectorResponse:
    pass


class ConnectorResponseMultiple(ConnectorResponse):

    def __init__(self, responses: List[ConnectorResponse]):
        self._responses = responses

    def get_responses(self) -> List[ConnectorResponse]:
        return self._responses


class ConnectorResponseText(ConnectorResponse):

    def __init__(self, text: str):
        self._text = text

    def get_text(self) -> str:
        return self._text


class ConnectorResponseOptions(ConnectorResponse):

    def __init__(self, options: List[str]):
        self._options = options

    def get_options(self) -> List[str]:
        return self._options


class ConnectorResponseFile(ConnectorResponse):

    def __init__(self, file_path: str):
        self._file_path = file_path

    def get_file_path(self) -> str:
        return self._file_path


class ConnectorResponseList(ConnectorResponse):

    def __init__(self, lista: List):
        self._list = lista

    def get_list(self) -> List:
        return self._list


class ConnectorResponseDictionary(ConnectorResponse):

    def __init__(self, dictionary: dict):
        self._dictionary = dictionary

    def get_dictionary(self) -> dict:
        return self._dictionary


class ConnectorResponseTable(ConnectorResponse):

    def __init__(self, headers: List[str], values: List[List]):
        self._headers = headers
        self._values = values

    def get_headers(self) -> List[str]:
        return self._headers

    def get_values(self) -> List[List]:
        return self._values


class Connector:

    def __init__(self, config: dict):
        self._config = config

    @abstractmethod
    def send_msg(self, msg: ConnectorResponse):
        raise NotImplemented

    @abstractmethod
    def send_response(self, msg: ConnectorResponse, connectorContext: ConnectorContext):
        raise NotImplemented

    @abstractmethod
    def run_listen(self, callback: ConnectorCallback):
        raise NotImplemented
