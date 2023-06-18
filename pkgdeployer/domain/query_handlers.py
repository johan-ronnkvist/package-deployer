from typing import Optional

from pkgdeployer.domain.package import Package
from pkgdeployer.domain.queries import FindPackageQuery
from pkgdeployer.repository.abstract_repository import UnitOfWork


def find_package(query: FindPackageQuery, unit_of_work: UnitOfWork) -> Optional[Package]:
    with unit_of_work:
        return unit_of_work.repository.find(query.uuid)





