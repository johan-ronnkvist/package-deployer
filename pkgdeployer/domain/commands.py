from dataclasses import dataclass
from uuid import UUID


class Command:
    """Commands represent the intent to change the state of the system."""
    pass


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
