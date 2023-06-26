from dataclasses import dataclass
from uuid import UUID

from pkgdeployer.domain.package import Package
from pkgdeployer.services.messaging import Command
from pkgdeployer.repository import Transaction


@dataclass(frozen=True)
class CreatePackageCommand(Command):
    uuid: UUID
    name: str


def create_package(command: CreatePackageCommand, transaction: Transaction) -> None:
    with transaction:
        transaction.packages.insert(Package(command.uuid, command.name))
        transaction.commit()


@dataclass(frozen=True)
class RemovePackageCommand(Command):
    uuid: UUID


def remove_package(command: RemovePackageCommand, transaction: Transaction) -> None:
    with transaction:
        transaction.packages.remove(command.uuid)
