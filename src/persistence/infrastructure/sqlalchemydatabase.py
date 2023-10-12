from abc import abstractmethod
from typing import List
from sqlalchemy import inspect, MetaData, text
from sqlalchemy import create_engine, Connection
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy_utils import database_exists, create_database
from src.persistence.domain.database import Database


class SQLAlchemyDatabase(Database):

    @abstractmethod
    def _get_url(self):
        pass

    def _connect(self) -> Connection:
        url = self._get_url()
        self._engine = create_engine(url, echo=self._config.get("debug", False))
        if not database_exists(self._engine.url):
            create_database(self._engine.url)
        connection = self._engine.connect()
        self._inspect = inspect(self._engine)
        self._metadata = MetaData()
        return connection

    def commit(self):
        self._connection.commit()

    def rollback(self):
        self._connection.rollback()

    def list_tables(self) -> List[str]:
        return self._inspect.get_table_names()

    def describe_table(self, table_name: str) -> List[tuple]:
        result_list = []
        for column in self._inspect.get_columns(table_name):
            result_list.append((column["name"], column["type"]))
        return result_list

    def check_if_table_exists(self, table_name: str) -> bool:
        return self._inspect.has_table(table_name)

    def create_table(self, entity: DeclarativeMeta) -> bool:
        self._metadata.create_all(self._engine, [entity.__table__])
        return True

    def exec_sql(self, query: str, commit: bool = True):
        res = self._connection.execute(text(query))
        if commit:
            self._connection.commit()
        return res

    """
    def insert_element(self, tabla: Tabla, element: dict):
        table = self._transform_table(tabla)
        res = self._connection.execute(insert(table), [element])
        self._connection.commit()
        return res

    def delete_element(self, tabla: Tabla, key):
        table = self._transform_table(tabla)
        Session = sessionmaker(bind=self._engine)
        session = Session()
        x = session.query(table).get(key)
        res = delete(x)
        session.commit()
        return res
    """
