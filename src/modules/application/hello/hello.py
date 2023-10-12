from src.connectors.domain.connector import ConnectorResponseText
from src.modules.application.hello.hellousecase import HelloUseCase
from src.modules.domain.module import Module
from src.modules.domain.modulecontext import ModuleContext
from src.modules.domain.statusenum import ModuleStatus


class Hello(Module):

    def __init__(self, config: dict):
        super().__init__("hello", self._get_help(), config)
        self._hello_use_case = HelloUseCase()

    @staticmethod
    def _get_help() -> str:
        str_response = "Saludarte"
        return str_response

    def on_message(self, module_context: ModuleContext):
        module_context.set_response(ConnectorResponseText(self._hello_use_case.get_saludo()))
        module_context.set_status(ModuleStatus.END)


