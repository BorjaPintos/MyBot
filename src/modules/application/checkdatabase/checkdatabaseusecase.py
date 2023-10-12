from datetime import datetime
import requests

from src.persistence.application.databasemanager import DatabaseManager


class CheckDatabaseUseCase:

    @staticmethod
    def check_database() -> dict:
        info_response = {
            "timestamp": datetime.now().strftime("%d-%m-%Y - %H:%M:%S"),
            "database_type": DatabaseManager.get_database().get_database_type(),
            "tables": DatabaseManager.list_tables()
        }

        return info_response

    @staticmethod
    def get_columns(table):
        return DatabaseManager.describe_table(table)
