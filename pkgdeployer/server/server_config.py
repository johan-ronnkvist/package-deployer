from uuid import uuid4

from domain.commands import CreatePackageCommand
from pkgdeployer.domain.queries import ListPackagesQuery, list_packages
from pkgdeployer.repository import Transaction, SQLTransaction, SQLModelSessionFactory
from pkgdeployer.services.ioc_container import IoCContainer
from pkgdeployer.services.messaging import MessageBus
from pkgdeployer.repository.sql_transaction import MockDataSessionFactory, SQLSessionFactory


def create_testing_content(container: IoCContainer):
    messages = container.resolve(MessageBus)
    for n in range(100):
        messages.publish(CreatePackageCommand(name=f"Package {n}", uuid=uuid4()))


def configure_messagebus(messagebus: MessageBus):
    messagebus.register_handler(ListPackagesQuery, list_packages)


def bootstrap() -> IoCContainer:
    container = IoCContainer()
    container.register(SQLSessionFactory, SQLModelSessionFactory(":memory:"))
    container.register(Transaction, SQLTransaction)
    container.register(MessageBus, MessageBus(container.resolve(Transaction)))

    configure_messagebus(container.resolve(MessageBus))



    return container

