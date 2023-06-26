import logging
from abc import ABC, abstractmethod
from typing import Optional, Protocol, runtime_checkable
from uuid import uuid4

from sqlmodel import create_engine, Session

from pkgdeployer.repository import Transaction
from pkgdeployer.repository.sql_repository import SQLRepository
from pkgdeployer.repository.sql_models import *

logging.root.setLevel(logging.DEBUG)
_logger = logging.getLogger(__name__)


@runtime_checkable
class SQLSessionFactory(Protocol):
    def create_session(self) -> Session:
        ...


class SQLModelSessionFactory:
    def __init__(self, database: str, **kwargs):
        _logger.info(f"Creating database sqlite:///{database}")
        self.engine = create_engine(f"sqlite:///{database}", **kwargs)
        SQLModel.metadata.create_all(self.engine)

    def create_session(self):
        return Session(self.engine)


class MockDataSessionFactory:
    def __init__(self, factory: SQLSessionFactory):
        self._factory = factory

        with self.create_session() as session:
            for n in range(100):
                session.add(SQLPackage(name=f"Package {n}", uuid=uuid4()))

    def create_session(self) -> Session:
        return self._factory.create_session()


class SQLTransaction(Transaction):
    def __init__(self, factory: SQLSessionFactory):
        self._factory = factory
        self._session: Optional[Session] = None
        self._packages: Optional[SQLRepository] = None

    def __enter__(self):
        self._session = self._factory.create_session()
        self._packages = SQLRepository(self._session)
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()
        self._packages = None

    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()

    @property
    def packages(self) -> SQLRepository:
        return self._packages
