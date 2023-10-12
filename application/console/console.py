from application.iapp import IApp
from loguru import logger

from src.core.application.core import Core


class Console(IApp):

    def run(self):
        logger.info("Start run")
        core = Core(self._config)
        core.run()
        logger.info("End run")
