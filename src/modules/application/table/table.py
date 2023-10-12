from src.connectors.domain.connector import ConnectorResponseTable
from src.modules.application.table.tableusecase import TableUseCase
from src.modules.domain.module import Module
from src.modules.domain.modulecontext import ModuleContext
from src.modules.domain.statusenum import ModuleStatus


class Table(Module):

    def __init__(self, config: dict):
        super().__init__("table", "Imprimir una tabla", config)
        self._table_use_case = TableUseCase()

    def on_message(self, module_context: ModuleContext):
        response_table = ConnectorResponseTable(headers=self._table_use_case.get_table_headers(),
                                                values=self._table_use_case.get_table_values())
        module_context.set_response(response_table)
        module_context.set_status(ModuleStatus.END)
