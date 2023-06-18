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
    def remove(self, uuid: UUID):
        raise NotImplementedError()

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def clear(self):
        raise NotImplementedError()

    def __contains__(self, uuid: UUID):
        return self.find(uuid) is not None

    def __len__(self):
        return self.count()


class UnitOfWork(ABC):
    def __init__(self, repository: Repository):
        """UnitOfWork is a context manager that provides access to a repository."""
        self._repository = repository

    def __enter__(self) -> 'UnitOfWork':
        """Enter the context manager, remember to commit any changes."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager, and rollback any uncommitted changes by default."""
        self.rollback()

    @property
    def repository(self) -> Repository:
        """Return the repository."""
        return self._repository

    @abstractmethod
    def commit(self):
        """Commit any changes."""
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
        """Rollback any changes."""
        raise NotImplementedError()
