import uuid

import pytest

from domain.package import Package
from pkgdeployer.repository import SQLModelSessionFactory, SQLTransaction, Transaction


@pytest.fixture
def package() -> Package:
    return Package(uuid.uuid4(), 'test_package')


@pytest.fixture
def database() -> SQLModelSessionFactory:
    return SQLModelSessionFactory(':memory:')


@pytest.fixture
def sql_transaction(database) -> Transaction:
    return SQLTransaction(database)


@pytest.fixture(params=[pytest.param("sql_transaction")])
def transaction(request):
    return request.getfixturevalue(request.param)
