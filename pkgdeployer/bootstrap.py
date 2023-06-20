import logging

from pkgdeployer.domain.queries import ListPackagesQuery, list_packages
from pkgdeployer.repository.abstract_repository import UnitOfWork, Repository
from pkgdeployer.repository.memory_repository import MemoryTransaction, MemoryRepository
from pkgdeployer.services.ioc_container import IoCContainer
from pkgdeployer.services.messaging import MessageBus

_logger = logging.getLogger(__name__)


def bootstrap() -> IoCContainer:
    _logger.info("Bootstrapping IoCContainer")
    container = IoCContainer()

    container.register(Repository, MemoryRepository)
    container.register(UnitOfWork, MemoryTransaction)
    container.register(MessageBus, MessageBus())

    return container
