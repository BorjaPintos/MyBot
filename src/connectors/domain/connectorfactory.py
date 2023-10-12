from src.connectors.domain.connector import Connector
from src.connectors.infrastructure.telegramconnector import TelegramConnector


class ConnectorFactory:

    @staticmethod
    def get_connector(config: dict) -> Connector:
        if "type" in config:
            _type = config["type"].lower()
            if _type == "telegram":
                return TelegramConnector(config[_type])
        raise NotImplemented
