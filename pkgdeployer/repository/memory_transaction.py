import copy

from repository import Transaction, Repository
from pkgdeployer.repository.memory_repository import MemoryRepository


class MemoryTransaction(Transaction):
    def __init__(self):
        super().__init__()
        self._current = MemoryRepository()
        self._original = MemoryRepository()

    def __enter__(self) -> Transaction:
        self._copy_repository(self._current, self._original)
        return self

    def commit(self):
        self._copy_repository(self._current, self._original)

    def rollback(self):
        self._copy_repository(self._original, self._current)

    @property
    def packages(self) -> Repository:
        return self._current

    @staticmethod
    def _copy_repository(source: 'MemoryRepository', destination: 'MemoryRepository'):
        destination.clear()
        for package in source.list(0, len(source)):
            destination.insert(copy.deepcopy(package))
