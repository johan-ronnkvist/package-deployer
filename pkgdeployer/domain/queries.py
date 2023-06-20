from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from pkgdeployer.domain.package import Package
from pkgdeployer.repository.abstract_repository import UnitOfWork
from pkgdeployer.services.messaging import Query


@dataclass(frozen=True)
class FindPackageQuery(Query):
    uuid: UUID


@dataclass(frozen=True)
class FindPackageResult:
    package: Optional[Package]


def find_package(query: FindPackageQuery, unit_of_work: UnitOfWork) -> FindPackageResult:
    with unit_of_work:
        return FindPackageResult(unit_of_work.repository.find(query.uuid))


@dataclass(frozen=True)
class ListPackagesQuery(Query):
    offset: int
    count: int


@dataclass(frozen=True)
class ListPackagesResult:
    packages: list[Package]


def list_packages(query: ListPackagesQuery, unit_of_work: UnitOfWork) -> ListPackagesResult:
    with unit_of_work:
        return ListPackagesResult(unit_of_work.repository.list(query.offset, query.count))
