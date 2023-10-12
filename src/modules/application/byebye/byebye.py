from src.connectors.domain.connector import ConnectorResponseText
from src.modules.application.byebye.byebyeusecase import ByeByeUseCase
from src.modules.domain.module import Module
from src.modules.domain.modulecontext import ModuleContext
from src.modules.domain.statusenum import ModuleStatus


class ByeBye(Module):

    def __init__(self, config: dict):
        super().__init__("byebye", "Despedirme", config)
        self._bye_bye_use_case = ByeByeUseCase()

    def on_message(self, module_context: ModuleContext):
        module_context.set_response(ConnectorResponseText(self._bye_bye_use_case.get_despedida()))
        module_context.set_status(ModuleStatus.END)

