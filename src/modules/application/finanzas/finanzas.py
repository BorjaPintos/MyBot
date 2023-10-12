from src.connectors.domain.connector import ConnectorResponseText
from src.modules.application.finanzas.finanzasusecase import FinanzasUseCase
from src.modules.domain.module import Module
from src.modules.domain.modulecontext import ModuleContext
from src.modules.domain.statusenum import ModuleStatus


class Finanzas(Module):

    def __init__(self, config: dict):
        super().__init__("finanzas", self._get_help(), config)
        self._finanzas_use_case = FinanzasUseCase()

    @staticmethod
    def _get_help() -> str:
        str_response = "Gestiona tus finanzas"
        return str_response

    def on_message(self, module_context: ModuleContext):
        if "query:" in module_context.get_msg():
            module_context.set_response(
                ConnectorResponseText("No implementado"))
        module_context.set_status(ModuleStatus.END)