from typing import Optional
from uuid import UUID

from pkgdeployer.domain.package import Package
from pkgdeployer.repository import Repository


class MemoryRepository(Repository):
    def __init__(self):
        self._packages = {}

    def insert(self, package: Package):
        if package.uuid in self._packages:
            raise KeyError(f'Package with UUID {package.uuid} already exists')
        self._packages[package.uuid] = package

    def find(self, uuid: UUID) -> Optional[Package]:
        return self._packages.get(uuid, None)

    def list(self, offset: int, count: int):
        return list(self._packages.values())[offset:offset+count]

    def delete(self, uuid: UUID):
        del self._packages[uuid]

    def count(self):
        return len(self._packages)

    def clear(self):
        self._packages.clear()

    def __len__(self) -> int:
        return len(self._packages)

