from src.connectors.domain.connectorcallback import ConnectorCallback
from src.connectors.domain.connectorcontext import ConnectorContext
from loguru import logger


class ConnectorCallbackEcho(ConnectorCallback):

    def on_message(self, connectorContext: ConnectorContext):
        logger.info("mensaje Recibido: {}", connectorContext.get_msg())
        connectorContext.get_connector().send_response(connectorContext.get_msg(), connectorContext)
