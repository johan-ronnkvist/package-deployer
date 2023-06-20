import logging
from typing import Optional

from sqlmodel import create_engine, Session, SQLModel

from repository.sql_repository import SQLRepository

_logger = logging.getLogger(__name__)


class SQLModelDatabase:
    def __init__(self, database: str):
        _logger.info(f"Creating database sqlite:///{database}")
        self.engine = create_engine(f"sqlite:///{database}")
        SQLModel.metadata.create_all(self.engine)

    def create_session(self):
        return Session(self.engine)


class SQLTransaction:
    def __init__(self, database: SQLModelDatabase):
        self._database = database
        self._session: Optional[Session] = None
        self._packages: Optional[SQLRepository] = None

    def __enter__(self):
        self._session = self._database.create_session()
        self._packages = SQLRepository(self._session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()

    @property
    def packages(self) -> SQLRepository:
        return self._packages
