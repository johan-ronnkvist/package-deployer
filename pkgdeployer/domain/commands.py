from dataclasses import dataclass
from uuid import UUID
from pkgdeployer.services.messaging import Command


@dataclass(frozen=True)
class CreatePackageCommand(Command):
    uuid: UUID
    name: str


@dataclass(frozen=True)
class RemovePackageCommand(Command):
    uuid: UUID


@dataclass(frozen=True)
class FindPackageCommand(Command):
    uuid: UUID
