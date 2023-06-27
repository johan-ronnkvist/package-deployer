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
    if not command.uuid:
        raise ValueError("uuid cannot be empty")
    if not command.name:
        raise ValueError("name cannot be empty")
    with transaction:
        transaction.packages.insert(Package(command.uuid, command.name))
        transaction.commit()


@dataclass(frozen=True)
class DeletePackageCommand(Command):
    uuid: UUID


def delete_package(command: DeletePackageCommand, transaction: Transaction) -> None:
    with transaction:
        transaction.packages.delete(command.uuid)
        transaction.commit()
