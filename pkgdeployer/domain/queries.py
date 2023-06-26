from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from pkgdeployer.domain.package import Package
from pkgdeployer.services.messaging import Query
from repository import Transaction


@dataclass(frozen=True)
class FindPackageQuery(Query):
    uuid: UUID


@dataclass(frozen=True)
class FindPackageResult:
    package: Optional[Package]


def find_package(query: FindPackageQuery, transaction: Transaction) -> FindPackageResult:
    with transaction:
        return FindPackageResult(transaction.packages.find(query.uuid))


@dataclass(frozen=True)
class ListPackagesQuery(Query):
    offset: int
    count: int


@dataclass(frozen=True)
class ListPackagesResult:
    packages: list[Package]


def list_packages(query: ListPackagesQuery, transaction: Transaction) -> ListPackagesResult:
    with transaction:
        return ListPackagesResult(transaction.packages.list(query.offset, query.count))
