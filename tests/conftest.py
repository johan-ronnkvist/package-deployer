import uuid

import pytest

from pkgdeployer.domain.queries import ListPackagesQuery, list_packages, FindPackageQuery, find_package
from pkgdeployer.domain.commands import CreatePackageCommand, create_package, DeletePackageCommand, delete_package
from pkgdeployer.domain.package import Package
from pkgdeployer.repository import SQLModelSessionFactory, SQLTransaction, Transaction
from pkgdeployer.services.messaging import MessageBus


@pytest.fixture
def package() -> Package:
    return Package(uuid.uuid4(), 'test_package')


@pytest.fixture
def session_factory() -> SQLModelSessionFactory:
    return SQLModelSessionFactory(':memory:')


@pytest.fixture
def sql_transaction(session_factory) -> Transaction:
    return SQLTransaction(session_factory)


@pytest.fixture(params=[pytest.param("sql_transaction")])
def transaction(request) -> Transaction:
    return request.getfixturevalue(request.param)


@pytest.fixture
def messagebus(transaction) -> MessageBus:
    messagebus = MessageBus(transaction)
    messagebus.register_handler(CreatePackageCommand, create_package)
    messagebus.register_handler(DeletePackageCommand, delete_package)
    messagebus.register_handler(ListPackagesQuery, list_packages)
    messagebus.register_handler(FindPackageQuery, find_package)

    return messagebus

