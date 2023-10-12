from src.connectors.domain.connector import ConnectorResponseText
from src.modules.application.ping.pingusecase import PingUseCase
from src.modules.domain.module import Module
from src.modules.domain.modulecontext import ModuleContext
from src.modules.domain.statusenum import ModuleStatus


class Ping(Module):

    def __init__(self, config: dict):
        super().__init__("ping", self._get_help(), config)
        self._ping_use_case = PingUseCase()

    @staticmethod
    def _get_help() -> str:
        str_response = "Devolverte pong"
        return str_response

    def on_message(self, module_context: ModuleContext):
        module_context.set_response(ConnectorResponseText(self._ping_use_case.do_ping(module_context.get_msg())))
        module_context.set_status(ModuleStatus.END)
