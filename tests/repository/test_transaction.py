import uuid

import pytest

from domain.package import Package
from repository import MemoryTransaction
from repository import SQLTransaction, SQLModelDatabase


@pytest.fixture
def package() -> Package:
    return Package(uuid.uuid4(), 'test_package')


@pytest.fixture
def database() -> SQLModelDatabase:
    return SQLModelDatabase(':memory:')


@pytest.fixture
def memory_transaction() -> MemoryTransaction:
    return MemoryTransaction()


@pytest.fixture
def sql_transaction(database) -> SQLTransaction:
    return SQLTransaction(database)


@pytest.fixture(params=[pytest.param("memory_transaction"), pytest.param("sql_transaction")])
def transaction(request):
    return request.getfixturevalue(request.param)


class TestTransactions:
    def test_transaction_rollback_as_default_behavior(self, transaction, package):
        with transaction as change:
            change.packages.insert(package)
            assert package in change.packages
        assert package not in change.packages

    def test_transaction_commit_persists_changes(self, transaction, package):
        with transaction:
            transaction.packages.insert(package)
            assert package in transaction.packages
            transaction.commit()
        assert package in transaction.packages

    def test_transaction_rollback_reverts_changes(self, transaction, package):
        with transaction:
            transaction.packages.insert(package)
            assert package in transaction.packages
            transaction.rollback()
            assert package not in transaction.packages
        assert package not in transaction.packages
