from typing import List

from sqlalchemy.orm import DeclarativeMeta

from src.persistence.domain.database import Database
from src.persistence.infrastructure.postgresdatabase import PostgresDatabase
from src.persistence.infrastructure.sqlitedatabase import SQLiteDatabase


class DatabaseManager:
    _DATABASE = None

    @staticmethod
    def init(config: dict):
        DatabaseManager._DATABASE = DatabaseManager.__init_database(config)

    @staticmethod
    def __init_database(config: dict) -> Database:
        switch_database = {
            'sqlite': SQLiteDatabase,
            'postgres': PostgresDatabase
        }
        return switch_database.get(config["type"])(config[config["type"]])

    @staticmethod
    def get_database() -> Database:
        if not DatabaseManager._DATABASE:
            raise Exception("DatabaseManager no está inicializado")
        return DatabaseManager._DATABASE

    @staticmethod
    def list_tables() -> List[str]:
        return DatabaseManager._DATABASE.list_tables()

    @staticmethod
    def describe_table(table_name: str) -> List[tuple]:
        """devuelve (nombre,tipo)"""
        return DatabaseManager._DATABASE.describe_table(table_name)

    @staticmethod
    def check_if_table_exist(table_name: str):
        return DatabaseManager._DATABASE.check_if_table_exist(table_name)

    @staticmethod
    def create_table(entity: DeclarativeMeta) -> bool:
        return DatabaseManager._DATABASE.create_table(entity)

    @staticmethod
    def exec_sql(query: str, commit: bool = True):
        return DatabaseManager._DATABASE.exec_sql(query, commit)

    @staticmethod
    def commit():
        return DatabaseManager._DATABASE.commit()

    @staticmethod
    def rollback():
        return DatabaseManager._DATABASE.rollback()