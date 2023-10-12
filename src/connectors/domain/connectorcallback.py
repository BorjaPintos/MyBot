from abc import abstractmethod

from src.connectors.domain.connectorcontext import ConnectorContext


class ConnectorCallback:

    def __init__(self):
        pass

    @abstractmethod
    def on_message(self, connectorContext: ConnectorContext):
        raise NotImplemented
