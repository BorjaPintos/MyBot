from src.connectors.domain.connector import ConnectorResponseText
from src.modules.domain.module import Module
from src.modules.domain.modulecontext import ModuleContext
from src.modules.domain.statusenum import ModuleStatus


class EmptyModule(Module):

    def __init__(self):
        super().__init__("Empty", self._get_help(), {"active": True})

    @staticmethod
    def _get_help() -> str:
        str_response = "Decirte que el módulo que buscas no está disponible"
        return str_response

    def on_message(self, module_context: ModuleContext):
        module_context.set_response(ConnectorResponseText(self._get_msg()))
        module_context.set_status(ModuleStatus.END)

    def inactive(self):
        pass

    @staticmethod
    def _get_msg() -> str:
        return "Creo que el modulo que buscas no está en el sistema"
