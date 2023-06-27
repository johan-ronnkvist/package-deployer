import logging
from uuid import uuid4

import pytest

from pkgdeployer.domain.package import Package
from pkgdeployer.domain.queries import ListPackagesQuery, list_packages, FindPackageQuery, find_package
from pkgdeployer.repository import Transaction

_logger = logging.getLogger(__name__)


def _populate(count: int, transaction: Transaction) -> Transaction:
    with transaction:
        for i in range(count):
            transaction.packages.insert(Package(uuid4(), f"Package {i}"))
        transaction.commit()
    return transaction


class TestListPackagesQuery:
    def test_list_with_offset_and_count(self, transaction):
        populated_transaction = _populate(50, transaction)
        result = list_packages(ListPackagesQuery(offset=1, count=5), populated_transaction)
        assert len(result.packages) == 5
        assert result.packages[0].name == "Package 1"
        assert result.packages[4].name == "Package 5"

    def test_list_more_items_than_exists(self, transaction):
        populated_transaction = _populate(50, transaction)
        with populated_transaction:
            count = len(populated_transaction.packages)

        result = list_packages(ListPackagesQuery(offset=0, count=count + 1), populated_transaction)
        assert len(result.packages) == count

    def test_list_with_offset_and_count_and_no_items(self, transaction):
        result = list_packages(ListPackagesQuery(offset=1, count=5), transaction)
        assert len(result.packages) == 0

    def test_list_with_offset_and_count_and_negative_offset(self, transaction):
        with pytest.raises(ValueError):
            list_packages(ListPackagesQuery(offset=-1, count=5), transaction)

    def test_list_with_offset_and_count_and_negative_count(self, transaction):
        with pytest.raises(ValueError):
            list_packages(ListPackagesQuery(offset=1, count=-5), transaction)


class TestFindPackageQuery:
    def test_find_existing_package(self, transaction):
        uuid = uuid4()
        with transaction:
            transaction.packages.insert(Package(uuid, "Test Package"))
            transaction.commit()
        result = find_package(FindPackageQuery(uuid), transaction)
        assert result.package is not None
        assert result.package.uuid == uuid

    def test_find_missing_package(self, transaction):
        result = find_package(FindPackageQuery(uuid4()), transaction)
        assert result.package is None

