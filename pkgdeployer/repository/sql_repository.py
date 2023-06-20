import abc
from typing import Optional
from uuid import UUID

from sqlmodel import Session

from domain.package import Package
from repository.abstract_repository import Repository
from repository.sql_models import SQLPackage


class SQLRepository(Repository):
    def __init__(self, session: Session):
        self._session = session

    def insert(self, package: Package):
        self._session.add(SQLPackage.from_orm(package))

    def find(self, uuid: UUID) -> Optional[Package]:
        return self._session.get(SQLPackage, uuid)

    def list(self, offset: int, count: int) -> list[Package]:
        return self._session.query(SQLPackage).offset(offset).limit(count).all()

    def delete(self, uuid: UUID):
        self._session.delete(self._session.get(SQLPackage, uuid))

    def clear(self):
        self._session.query(SQLPackage).delete()

    def __len__(self) -> int:
        return self._session.query(SQLPackage).count()


