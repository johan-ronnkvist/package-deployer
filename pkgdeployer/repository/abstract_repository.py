from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from pkgdeployer.domain.package import Package


class Repository(ABC):
    @abstractmethod
    def insert(self, package: Package):
        raise NotImplementedError()

    @abstractmethod
    def find(self, uuid: UUID) -> Optional[Package]:
        raise NotImplementedError()

    @abstractmethod
    def list(self, offset: int, count: int) -> list[Package]:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, uuid: UUID):
        raise NotImplementedError()

    @abstractmethod
    def clear(self):
        raise NotImplementedError()

    def __contains__(self, package: Package) -> bool:
        return self.find(package.uuid) is not None

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError()



