from src.connectors.domain.connector import ConnectorResponseDictionary, ConnectorResponseMultiple, \
    ConnectorResponseList, ConnectorResponseText, ConnectorResponseTable
from src.modules.application.checkdatabase.checkdatabaseusecase import CheckDatabaseUseCase
from src.modules.domain.module import Module
from src.modules.domain.modulecontext import ModuleContext
from src.modules.domain.statusenum import ModuleStatus
import re


class CheckDatabase(Module):

    def __init__(self, config: dict):
        super().__init__("checkdatabase", self._get_help(), config)
        self._check_database_use_case = CheckDatabaseUseCase()

    @staticmethod
    def _get_help() -> str:
        str_response = "Comprobar si la base de datos está ok"
        return str_response

    def on_message(self, module_context: ModuleContext):
        multiple_response = ConnectorResponseMultiple([])
        info_base = self._check_database_use_case.check_database()
        multiple_response.add_response(ConnectorResponseDictionary(info_base))
        for table in info_base["tables"]:
            multiple_response.add_response(ConnectorResponseText(table))
            columns = self._check_database_use_case.get_columns(table)
            headers = []
            values = [[]]
            for column_name, tipo_columna in columns:
                headers.append(column_name)
                values[0].append(tipo_columna)
            multiple_response.add_response(
                ConnectorResponseTable(headers=headers, values=values))
        module_context.set_response(multiple_response)
        module_context.set_status(ModuleStatus.END)
