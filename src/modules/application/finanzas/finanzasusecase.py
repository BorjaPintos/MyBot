import traceback

from loguru import logger
from sqlalchemy.orm import DeclarativeMeta

from src.modules.application.finanzas.orm.categoriagasto import CategoriaGasto
from src.modules.application.finanzas.orm.categoriaingreso import CategoriaIngreso
from src.modules.application.finanzas.orm.cuenta import Cuenta
from src.modules.application.finanzas.orm.monedero import Monedero
from src.modules.application.finanzas.orm.operaciongasto import OperacionGasto
from src.modules.application.finanzas.orm.operacioningreso import OperacionIngreso
from src.persistence.application.databasemanager import DatabaseManager
from src.persistence.infrastructure.orm.baseentity import BaseEntity


class FinanzasUseCase:
    _SQL_BASE_FOLDER = "./src/modules/application/finanzas/sql/"
    _ELEMENT_TO_INIT = {
        Cuenta: "cuenta.sql",
        Monedero: "monedero.sql",
        CategoriaGasto: "categoriagasto.sql",
        CategoriaIngreso: "categoriaingreso.sql",
        OperacionGasto: None,
        OperacionIngreso: None
    }

    def __init__(self):
        self._check_database()

    def _check_database(self):
        try:
            for table in self._ELEMENT_TO_INIT.keys():
                self._check_cuenta(table, self._ELEMENT_TO_INIT[table])
                DatabaseManager.commit()
        except Exception as e:
            DatabaseManager.rollback()
            traceback.print_exc()
            logger.error(e)

    def _check_cuenta(self, table: BaseEntity, file: str):
        if not DatabaseManager.check_if_table_exist(table.__tablename__):
            DatabaseManager.create_table(table)
            if file:
                with open(self._SQL_BASE_FOLDER + file, encoding="utf-8") as file:
                    seguir = True
                    while seguir:
                        query = file.readline()
                        if query:
                            DatabaseManager.exec_sql(query, commit=False)
                        else:
                            seguir = False
