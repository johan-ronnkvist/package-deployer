import os
from uuid import uuid4

from pkgdeployer.domain.commands import CreatePackageCommand, create_package
from pkgdeployer.domain.queries import ListPackagesQuery, list_packages, FindPackageQuery, find_package
from pkgdeployer.repository import Transaction, SQLTransaction, SQLModelSessionFactory
from pkgdeployer.services.ioc_container import IoCContainer
from pkgdeployer.services.messaging import MessageBus
from pkgdeployer.repository.sql_transaction import MockDataSessionFactory, SQLSessionFactory
from pkgdeployer.server import configuration


def create_testing_content(container: IoCContainer):
    messages = container.resolve(MessageBus)
    for n in range(100):
        messages.publish(CreatePackageCommand(name=f"Package {n}", uuid=uuid4()))


def configure_messagebus(messagebus: MessageBus):
    messagebus.register_handler(ListPackagesQuery, list_packages)
    messagebus.register_handler(CreatePackageCommand, create_package)
    messagebus.register_handler(FindPackageQuery, find_package)


def bootstrap() -> IoCContainer:
    container = IoCContainer()
    database = configuration.database_url()
    # container.register(SQLSessionFactory, MockDataSessionFactory(SQLModelSessionFactory(database, echo=True)))
    container.register(SQLSessionFactory, SQLModelSessionFactory(database, echo=True))
    container.register(Transaction, SQLTransaction)
    container.register(MessageBus, MessageBus(container.resolve(Transaction)))

    configure_messagebus(container.resolve(MessageBus))

    # create_testing_content(container)

    return container

