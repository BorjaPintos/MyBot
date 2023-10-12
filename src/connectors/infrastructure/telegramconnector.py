import tempfile
from os import path

from src.connectors.domain.connector import Connector, ConnectorResponse, ConnectorResponseText, \
    ConnectorResponseMultiple, ConnectorResponseDictionary, ConnectorResponseTable
from src.connectors.domain.connectorcallback import ConnectorCallback
from loguru import logger
import telegram
from telegram.ext import MessageHandler, ApplicationBuilder, ContextTypes, filters, Application
import asyncio
import whisper

from src.connectors.domain.connectorcontext import ConnectorContext

default_config_whisper = {
    "model_type": "tiny",
    "use_fp16": False,
    "language": None
}
TELEGRAMLINES = 64


class TelegramConnector(Connector):

    def __init__(self, config: dict):
        super().__init__(config)
        self._token = config["token"]
        self._chat_id = config["chat_id"]

        config_whisper = config.get("whisper", default_config_whisper)
        self._use_fp16 = config_whisper.get("use_fp16")
        self._default_language = config_whisper.get("language")
        self._whisper_model = whisper.load_model(config_whisper.get("model_type"))

        self._bot = telegram.Bot(self._token)
        self.send_msg(ConnectorResponseText("Iniciado!"))
        self._application = None
        logger.info("Conector Telegram iniciado")

    def send_msg(self, response: ConnectorResponse):
        if isinstance(response, ConnectorResponseText):
            asyncio.run(self._async_send_text(response.get_text()))

    def send_response(self, response: ConnectorResponse, connectorContext: ConnectorContext):
        loop = asyncio.get_running_loop()
        if loop.is_running():
            tsk = loop.create_task(self._async_send_response(response, connectorContext))
            tsk.done()
        else:
            asyncio.run(self._async_send_response(response, connectorContext))

    @staticmethod
    async def _async_send_response(response: ConnectorResponse, connector_context: ConnectorContext):
        if isinstance(response, ConnectorResponseMultiple):
            for connector_response in response.get_responses():
                connector_context.get_connector().send_response(connector_response, connector_context)
        if isinstance(response, ConnectorResponseText):
            await TelegramConnector._send_response_text(connector_context, response.get_text())
        if isinstance(response, ConnectorResponseDictionary):
            headers = list(response.get_dictionary().keys())
            values = [list(response.get_dictionary().values())]
            str_table = TelegramConnector.format_table(headers, values)
            await TelegramConnector._send_response_text(connector_context, str_table)
        if isinstance(response, ConnectorResponseTable):
            str_table = TelegramConnector.format_table(response.get_headers(), response.get_values())
            await TelegramConnector._send_response_text(connector_context, str_table)

    @staticmethod
    async def _send_response_text(connector_context, text: str):
        await connector_context.get_session().bot.send_message(text=text,
                                                               chat_id=connector_context.get_room_id(),
                                                               reply_to_message_id=connector_context.get_msg_id())

    async def _async_send_text(self, text: str):
        async with self._bot:
            await self._bot.send_message(text=text, chat_id=self._chat_id)

    def __get_application(self) -> Application:
        if not self._application:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self._application = ApplicationBuilder().token(self._token).build()
        return self._application

    def run_listen(self, callback: ConnectorCallback):

        message_hander = MessageHandler(
            filters.VOICE | filters.TEXT | filters.COMMAND |
            filters.Chat(chat_id=self._chat_id),
            self._on_message(callback))
        application = self.__get_application()
        application.add_handler(message_hander)
        logger.info("Empezando run_polling")
        application.run_polling()

    def _on_message(self, callback: ConnectorCallback):

        async def __on_message(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
            chat_id = update.effective_chat.id
            user_id = update.effective_user.id
            user_name = update.effective_user.name
            message_id = update.message.message_id
            if update.effective_message.voice:
                voice_id = update.effective_message.voice.file_id
                voice_file = await context.bot.get_file(voice_id)
                with tempfile.TemporaryDirectory() as destination:
                    path_file = await voice_file.download_to_drive(path.join(destination, voice_file.file_unique_id))
                    message = \
                        self._whisper_model.transcribe(str(path_file), fp16=self._use_fp16,
                                                       language=self._default_language)[
                            "text"]
            else:
                message = update.message.text
            logger.debug(
                "Mensaje recibido de: chat_id: {} del usuario '{}' con id {}".format(chat_id, user_name, user_id))
            logger.debug(message)
            connector_context = ConnectorContext(message, message_id, user_id, user_name, chat_id, self, context)
            callback.on_message(connector_context)

        return __on_message

    @staticmethod
    def format_table(headers, values):
        # metodo de chatgpt y colaboración de sdvicente

        # Obtener la longitud máxima de cada columna
        column_widths = [max(len(str(value)) for value in column) for column in zip(headers, *values)]

        # Crear la línea de separación entre las cabeceras y los valores
        separator = "+" + "+".join("-" * (width + 2) for width in column_widths) + "+"

        # Crear la representación de la tabla
        table = []
        table.append(separator)
        table.append("| " + " | ".join(header.ljust(width) for header, width in zip(headers, column_widths)) + " |")
        table.append(separator)
        for row in values:
            table.append("| " + " | ".join(str(value).ljust(width) for value, width in zip(row, column_widths)) + " |")
        table.append(separator)
        str_table = "\n".join(table)
        logger.debug("\n"+str_table)
        return str_table
