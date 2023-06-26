import logging
import uuid

from domain.package import Package
from pkgdeployer.services.ioc_container import IoCContainer
from pkgdeployer.services.messaging import MessageBus
from repository import SQLModelSessionFactory, Transaction, SQLTransaction

_logger = logging.getLogger(__name__)


def bootstrap() -> IoCContainer:
    _logger.info("Bootstrapping IoCContainer")
    container = IoCContainer()

    container.register(SQLModelSessionFactory, SQLModelSessionFactory(':memory:'))
    container.register(Transaction, SQLTransaction)
    container.register(MessageBus, MessageBus(container.resolve(Transaction)))

    init = container.resolve(Transaction)
    with init:
        for n in range(100):
            init.packages.insert(Package(uuid.uuid4(), f"sample_pkg_{n}"))
        init.commit()

    return container
