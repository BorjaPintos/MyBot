from src.connectors.domain.connector import ConnectorResponseText, ConnectorResponseDictionary
from src.modules.application.checkurl.checkurlusecase import CheckURLUseCase
from src.modules.domain.module import Module
from src.modules.domain.modulecontext import ModuleContext
from src.modules.domain.statusenum import ModuleStatus
import re


class CheckURL(Module):

    def __init__(self, config: dict):
        super().__init__("checkurl", self._get_help(), config)
        self._check_url_use_case = CheckURLUseCase()
        self._url_patter = re.compile(r"""(([a-zA-Z]+://){1}[^'"\s]+)""")

    @staticmethod
    def _get_help() -> str:
        str_response = "Comprobar si una URL está activa"
        return str_response

    def on_message(self, module_context: ModuleContext):
        url = self._extract_url(module_context.get_msg())
        if url:
            module_context.set_response(ConnectorResponseDictionary(self._check_url_use_case.check_url(url)))
            module_context.set_status(ModuleStatus.END)
        else:
            module_context.set_response(ConnectorResponseText("Dime la url por favor (debe empezar por http/https)"))
            module_context.set_status(ModuleStatus.DURING)

    def _extract_url(self, msg: str) -> str:
        group_list = re.findall(self._url_patter, msg)
        if group_list:
            return group_list[0][0]

