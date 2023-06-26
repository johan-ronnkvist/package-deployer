import abc
from typing import Optional
from uuid import UUID

from sqlmodel import Session

from pkgdeployer.domain.package import Package
from pkgdeployer.repository.abstract_repository import Repository, PackageInsertError, PackageDeleteError
from pkgdeployer.repository.sql_models import SQLPackage


class SQLRepository(Repository):
    def __init__(self, session: Session):
        self._session = session

    def insert(self, package: Package):
        if self.find(package.uuid) is not None:
            raise PackageInsertError(f'Package with UUID {package.uuid} already exists')

        self._session.add(SQLPackage.from_orm(package))

    def find(self, uuid: UUID) -> Optional[Package]:
        found = self._session.get(SQLPackage, uuid)
        if found:
            return Package(**found.dict())
        else:
            return None

    def list(self, offset: int, count: int) -> list[Package]:
        return self._session.query(SQLPackage).offset(offset).limit(count).all()

    def delete(self, uuid: UUID):
        found = self._session.get(SQLPackage, uuid)
        if not found:
            raise PackageDeleteError(f'Package with UUID {uuid} not found')
        else:
            self._session.delete(found)

    def clear(self):
        self._session.query(SQLPackage).delete()

    def __len__(self) -> int:
        return self._session.query(SQLPackage).count()


