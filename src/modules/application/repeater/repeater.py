from src.connectors.domain.connector import ConnectorResponseText
from src.modules.application.repeater.repeaterusecase import RepeaterUseCase
from src.modules.domain.module import Module
from src.modules.domain.modulecontext import ModuleContext
from src.modules.domain.statusenum import ModuleStatus


class Repeater(Module):

    def __init__(self, config: dict):
        super().__init__("repeater", self._get_help(), config)
        self._repeater_use_case = RepeaterUseCase()

    @staticmethod
    def _get_help() -> str:
        str_response = "Repetir lo que dices"
        return str_response

    def on_message(self, module_context: ModuleContext):
        module_context.set_response(
            ConnectorResponseText(self._repeater_use_case.do_repeater(module_context.get_msg())))
        module_context.set_status(ModuleStatus.DURING)
