from uuid import uuid4

import pytest

from pkgdeployer.domain.commands import CreatePackageCommand, create_package, delete_package, DeletePackageCommand
from pkgdeployer.repository import PackageInsertError, PackageDeleteError


class TestCreatePackageCommand:
    def test_create_package(self, transaction):
        cmd = CreatePackageCommand(uuid=uuid4(), name="Test Package")
        assert cmd.uuid is not None
        assert cmd.name == "Test Package"
        with transaction:
            assert transaction.packages.find(cmd.uuid) is None
        create_package(cmd, transaction)
        with transaction:
            assert transaction.packages.find(cmd.uuid) is not None

    def test_create_duplicated_package(self, transaction):
        cmd = CreatePackageCommand(uuid=uuid4(), name="Test Package")
        with transaction:
            assert transaction.packages.find(cmd.uuid) is None
        create_package(cmd, transaction)
        with transaction:
            assert transaction.packages.find(cmd.uuid) is not None
        with pytest.raises(PackageInsertError):
            create_package(cmd, transaction)

    def test_create_package_with_empty_name(self, transaction):
        cmd = CreatePackageCommand(uuid=uuid4(), name="")
        with pytest.raises(ValueError):
            create_package(cmd, transaction)

    def test_create_package_with_empty_uuid(self, transaction):
        cmd = CreatePackageCommand(uuid=None, name="Test Package")
        with pytest.raises(ValueError):
            create_package(cmd, transaction)


class TestDeletePackageCommand:
    def test_delete_package(self, transaction):
        uuid = uuid4()
        create_package(CreatePackageCommand(uuid, "Test Package"), transaction)
        with transaction:
            assert transaction.packages.find(uuid) is not None
        delete_package(DeletePackageCommand(uuid), transaction)
        with transaction:
            assert transaction.packages.find(uuid) is None

    def test_delete_package_that_does_not_exist(self, transaction):
        uuid = uuid4()
        with pytest.raises(PackageDeleteError):
            delete_package(DeletePackageCommand(uuid), transaction)
