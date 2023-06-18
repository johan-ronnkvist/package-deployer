import copy
from uuid import UUID

from pkgdeployer.domain.package import Package
from pkgdeployer.repository.abstract_repository import Repository, UnitOfWork


class MemoryRepository(Repository):
    def __init__(self):
        self._packages = {}

    def insert(self, package: Package):
        self._packages[package.uuid] = package

    def find(self, uuid: UUID):
        return self._packages.get(uuid)

    def list(self, offset: int, count: int):
        return list(self._packages.values())[offset:offset+count]

    def remove(self, uuid: UUID):
        del self._packages[uuid]

    def count(self):
        return len(self._packages)

    def clear(self):
        self._packages.clear()


class MemoryUnitOfWork(UnitOfWork):
    def __init__(self):
        super().__init__(MemoryRepository())
        self._copy = MemoryRepository()

    def __enter__(self) -> 'UnitOfWork':
        for package in self._repository.list(0, len(self._repository)):
            self._copy.insert(copy.deepcopy(package))
        return super().__enter__()

    @property
    def repository(self) -> Repository:
        return self._copy

    def commit(self):
        self._repository = self._copy

    def rollback(self):
        """Automatically rollback any changes by default."""
        pass
