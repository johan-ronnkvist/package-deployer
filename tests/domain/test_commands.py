from uuid import uuid4

from domain.commands import CreatePackageCommand, create_package


def test_create_package(transaction):
    cmd = CreatePackageCommand(uuid=uuid4(), name="Test Package")
    with transaction:
        assert transaction.packages.find(cmd.uuid) is None
    create_package(cmd, transaction)
    with transaction:
        assert transaction.packages.find(cmd.uuid) is not None

