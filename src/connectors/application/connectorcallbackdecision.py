from typing import List, Optional
from loguru import logger
from src.connectors.domain.connectorcallback import ConnectorCallback
from src.connectors.domain.connectorcontext import ConnectorContext
from src.modules.domain.module import Module
from src.modules.domain.modulecontext import ModuleContext
from src.modules.domain.statusenum import ModuleStatus


class ConnectorCallbackDecision(ConnectorCallback):

    def __init__(self, active_modules: List[Module], inactive_modules: List[Module]):
        super().__init__()
        self._active_modules = active_modules
        self._inactive_modules = inactive_modules
        self._active_user_module = {}

    def on_message(self, connectorContext: ConnectorContext):
        logger.info("Mensaje Recibido: {}", connectorContext.get_msg())
        msg = connectorContext.get_msg()
        if "end" in msg.lower() or "fin" in msg.lower():
            self.__end_module(connectorContext)
        else:
            self.usar_modulo(connectorContext, msg)

    def usar_modulo(self, connectorContext, msg):
        module_context = self.__get_active_mode(connectorContext.get_user_id(), connectorContext.get_room_id())
        if not module_context:
            module = self.__decide_module(msg)
            module_context = ModuleContext(msg=msg, user_id=connectorContext.get_user_id(),
                                           username=connectorContext.get_username(), module=module)
            self.__add_active_module(connectorContext.get_user_id(), connectorContext.get_room_id(), module_context)
        module_context.set_msg(connectorContext.get_msg())
        module_context.get_module().on_message(module_context)
        if module_context.get_response():
            connectorContext.get_connector().send_response(module_context.get_response(), connectorContext)
        else:
            self.__end_module(connectorContext)
        if module_context.get_status() == ModuleStatus.END:
            self.__end_module(connectorContext)

    def __end_module(self, connectorContext: ConnectorContext):
        self.__remove_active_mode(connectorContext.get_user_id(), connectorContext.get_room_id())

    def __add_active_module(self, user_id, room_id, module_context: ModuleContext):
        if user_id not in self._active_user_module:
            self._active_user_module[user_id] = {room_id: module_context}
        else:
            self._active_user_module[user_id][room_id] = module_context
        logger.info("Modulo {} activo para el usuario {}".format(module_context.get_module().get_name(),
                                                                 module_context.get_username()))

    def __get_active_mode(self, user_id, room_id) -> Optional[ModuleContext]:
        if user_id in self._active_user_module:
            if room_id in self._active_user_module[user_id]:
                return self._active_user_module[user_id][room_id]
        return None

    def __remove_active_mode(self, user_id, room_id):
        if user_id in self._active_user_module:
            if room_id in self._active_user_module[user_id]:
                logger.info("Modulo {} terminado para el usuario {}".format(
                    self._active_user_module[user_id][room_id].get_module().get_name(),
                    self._active_user_module[user_id][room_id].get_username()))
                del self._active_user_module[user_id][room_id]

    def __decide_module(self, msg: str) -> Module:
        module_max_punctuation_index = 0
        max_punctuation = 0
        index = 0
        for module in self._active_modules:
            punctuation = self.__get_punctuation(module, msg)
            logger.debug("El Modulo {} tuvo una puntuación de: {}".format(module.get_name(), punctuation))
            if punctuation > max_punctuation:
                max_punctuation = punctuation
                module_max_punctuation_index = index
            index += 1
        logger.debug(
                "El Modulo seleccionado es:{}".format(self._active_modules[module_max_punctuation_index].get_name()))
        return self._active_modules[module_max_punctuation_index]

    @staticmethod
    def __get_punctuation(module: Module, msg: str) -> int:
        punctuation = 0
        lower_msg = msg.lower()
        for word in module.get_words_to_match():
            if word.lower() in lower_msg:
                punctuation += 1
        return punctuation
