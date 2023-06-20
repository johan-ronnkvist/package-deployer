from abc import ABC, abstractmethod


class Transaction(ABC):
    """Abstract transaction on the underlying data storage."""

    def __enter__(self) -> 'Transaction':
        """Enter the context manager, remember to commit any changes."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager, and rollback any uncommitted changes by default."""
        self.rollback()

    @property
    @abstractmethod
    def packages(self) -> 'Repository':
        """Provides access to the repository."""
        raise NotImplementedError()

    @abstractmethod
    def commit(self):
        """Commit any changes."""
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
        """Rollback any changes."""
        raise NotImplementedError()