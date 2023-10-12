from abc import abstractmethod
from typing import List

from src.modules.domain.modulecontext import ModuleContext


class Module:

    def __init__(self, name: str, help_description: str, config: dict):
        self._name = name
        self._help_description = help_description
        self._config = config
        self._active = config["active"]
        self._words_to_match = config.get("words_to_match", [])

    def get_name(self):
        return self._name

    def get_words_to_match(self) -> List[str]:
        return self._words_to_match

    def is_active(self) -> bool:
        return self._active

    def inactive(self):
        self._active = False

    def activate(self):
        self._active = True

    @abstractmethod
    def on_message(self, module_context: ModuleContext):
        raise NotImplemented

    def get_help_description(self):
        return self._help_description
