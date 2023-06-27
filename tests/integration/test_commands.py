from uuid import uuid4

import pytest

from pkgdeployer.domain.commands import CreatePackageCommand, DeletePackageCommand
from pkgdeployer.domain.queries import FindPackageQuery, ListPackagesQuery
from pkgdeployer.repository import PackageDeleteError


class TestEndpoints:
    def test_create_package(self, messagebus, transaction):
        uuid = uuid4()
        messagebus.publish(CreatePackageCommand(uuid=uuid, name="Test Package"))
        with transaction:
            assert transaction.packages.find(uuid) is not None

    def test_delete_existing_package(self, messagebus, transaction):
        uuid = uuid4()
        messagebus.publish(CreatePackageCommand(uuid=uuid, name="Test Package"))
        with transaction:
            assert transaction.packages.find(uuid) is not None
        messagebus.publish(DeletePackageCommand(uuid))
        with transaction:
            assert transaction.packages.find(uuid) is None

    def test_delete_missing_package(self, messagebus, transaction):
        uuid = uuid4()
        with transaction:
            assert transaction.packages.find(uuid) is None
        with pytest.raises(PackageDeleteError):
            messagebus.publish(DeletePackageCommand(uuid))
        with transaction:
            assert transaction.packages.find(uuid) is None

    def test_find_existing_package(self, messagebus, transaction):
        uuid = uuid4()
        messagebus.publish(CreatePackageCommand(uuid=uuid, name="Test Package"))
        with transaction:
            assert transaction.packages.find(uuid) is not None
        result = messagebus.publish(FindPackageQuery(uuid))
        assert result.package.uuid == uuid
        assert result.package.name == "Test Package"

    def test_find_missing_package(self, messagebus, transaction):
        result = messagebus.publish(FindPackageQuery(uuid4()))
        assert result.package is None

    def test_list_existing_packages(self, messagebus, transaction):
        uuid1 = uuid4()
        uuid2 = uuid4()
        messagebus.publish(CreatePackageCommand(uuid=uuid1, name="Test Package 1"))
        messagebus.publish(CreatePackageCommand(uuid=uuid2, name="Test Package 2"))
        with transaction:
            assert transaction.packages.find(uuid1) is not None
            assert transaction.packages.find(uuid2) is not None
        result = messagebus.publish(ListPackagesQuery(offset=0, count=10))
        assert len(result.packages) == 2
        assert result.packages[0].uuid == uuid1
        assert result.packages[0].name == "Test Package 1"
        assert result.packages[1].uuid == uuid2
        assert result.packages[1].name == "Test Package 2"
