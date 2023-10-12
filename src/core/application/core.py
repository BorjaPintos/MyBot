import importlib
import traceback

from loguru import logger
from src.connectors.application.connectorcallbackdecision import ConnectorCallbackDecision
from src.connectors.domain.connectorfactory import ConnectorFactory
import inspect

from src.core.application.coremodule import CoreModule
from src.core.application.emptymodule import EmptyModule
from src.persistence.application.databasemanager import DatabaseManager

MODULES_PACKAGE = "src.modules.application"


class Core:

    def __init__(self, config: dict):
        self._config = config
        self._database = self.__init_database(self._config["database"])
        self._connector = self.__get_connector(self._config["connector"])
        self._active_modules = [EmptyModule()]
        self._inactive_modules = []
        self.__load_modules(self._config["modules"])
        self._active_modules.append(CoreModule(self._active_modules, self._inactive_modules))

    def run(self):
        decision_callback = ConnectorCallbackDecision(self._active_modules, self._inactive_modules)
        self._connector.run_listen(decision_callback)

    @staticmethod
    def __init_database(config_database: dict):
        return DatabaseManager.init(config_database)

    @staticmethod
    def __get_connector(config_conector: dict):
        return ConnectorFactory.get_connector(config_conector)

    def __load_modules(self, modules_config: dict):
        for module_config in modules_config:
            try:
                dynamic_mod = importlib.import_module(
                    # src.modules.application.example.example
                    MODULES_PACKAGE + "." + module_config["name"] + "." + module_config["name"])
                classes = inspect.getmembers(dynamic_mod, inspect.isclass)
                # por regla general, observo que se pone de último, pero no tiene por qué ser así siempre
                # así que haciendo un reverse lo podemos encontrar de primero
                classes.reverse()
                for name, py_mod in classes:
                    if name.lower() == module_config["name"]:
                        module = py_mod(module_config)
                        if module.is_active():
                            self._active_modules.append(module)
                            logger.info("Módulo {} cargado".format(module_config["name"]))
                        else:
                            self._inactive_modules.append(module)
                            logger.info("Módulo {} cargado pero inactivo".format(module_config["name"]))
                        break
            except Exception:
                traceback.print_exc()
                logger.error("El módulo {} no se pudo cargar".format(module_config["name"]))
