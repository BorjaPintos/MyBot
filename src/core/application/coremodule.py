from typing import List

from src.connectors.domain.connector import ConnectorResponseText
from src.modules.domain.module import Module
from src.modules.domain.modulecontext import ModuleContext
from src.modules.domain.statusenum import ModuleStatus


class CoreModule(Module):

    def __init__(self, active_modules: List[Module], inactive_modules: List[Module]):
        super().__init__("core", self._get_help(), {
            "name": "core",
            "words_to_match": [
                "que puedes hacer", "qué puedes hacer",
                "puedes", "hacer", "ayuda", "help", "/help", "/ayuda",
                "activa", "desactiva", "módulo", "modulo",
                "modulos", "módulos", "listar", "lista",
                "listame", "lístame", "información", "informacion"
            ],
            "active": True
        })
        self._active_modules = active_modules
        self._inactive_modules = inactive_modules

    def on_message(self, module_context: ModuleContext):
        module_context.set_response(ConnectorResponseText(self._get_msg()))
        module_context.set_status(ModuleStatus.END)

    def inactive(self):
        pass

    @staticmethod
    def _get_help() -> str:
        str_response = "Listar los módulos activos, "
        str_response += "Listar los módulos inactivos, "
        str_response += "Activar módulos, "
        str_response += "Desactivar módulos"
        return str_response

    def _get_msg(self) -> str:
        str_response = "Puedo realizar distintas tareas como:\n"
        for module in self._active_modules:
            str_response += "- " + module.get_name() + ": [" + module.get_help_description() + "]\n"
        return str_response
