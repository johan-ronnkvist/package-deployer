import uuid
import os.path as path

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
def memory_session() -> SQLModelSessionFactory:
    return SQLModelSessionFactory(':memory:')


@pytest.fixture
def file_session(tmp_path) -> SQLModelSessionFactory:
    return SQLModelSessionFactory(path.join(tmp_path, 'test.db'))


@pytest.fixture
def sql_memory_transaction(memory_session) -> Transaction:
    return SQLTransaction(memory_session)


@pytest.fixture
def sql_file_transaction(file_session) -> Transaction:
    return SQLTransaction(file_session)


@pytest.fixture(params=[pytest.param("sql_memory_transaction"), pytest.param("sql_file_transaction")])
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

