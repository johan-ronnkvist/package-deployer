from pkgdeployer.domain.commands import CreatePackageCommand
from pkgdeployer.domain.package import Package
from pkgdeployer.repository.abstract_repository import UnitOfWork


def create_package(command: CreatePackageCommand, unit_of_work: UnitOfWork):
    with unit_of_work:
        try:
            unit_of_work.repository.insert(Package(command.uuid, command.name))
        except KeyError:
            raise ValueError(f'Package with UUID {command.uuid} already exists')