import uuid

import pytest

from pkgdeployer.repository import PackageInsertError, PackageDeleteError


class TestRepository:
    def test_insert_success(self, package, transaction):
        with transaction:
            repository = transaction.packages
            assert len(repository) == 0
            assert package not in repository
            repository.insert(package)
            assert len(repository) == 1
            assert package in repository

    def test_insert_duplicate(self, transaction, package):
        with transaction:
            repository = transaction.packages
            repository.insert(package)
            with pytest.raises(PackageInsertError):
                repository.insert(package)

    def test_find_success(self, transaction, package):
        with transaction:
            repository = transaction.packages
            repository.insert(package)
            result = repository.find(package.uuid)
            assert result is not None
            assert result == package

    def test_find_failure(self, transaction, package):
        with transaction:
            repo = transaction.packages
            invalid_uuid = uuid.uuid4()
            result = repo.find(invalid_uuid)
            assert result is None

    def test_remove_requires_commit(self, transaction, package):
        with transaction:
            repo = transaction.packages
            repo.insert(package)
            assert package in repo
            repo.delete(package.uuid)
            assert package in repo
            transaction.commit()
            assert package not in repo

    def test_remove_failure(self, transaction, package):
        with transaction:
            repo = transaction.packages
            with pytest.raises(PackageDeleteError):
                repo.delete(package.uuid)

    def test_clear(self, transaction, package):
        with transaction:
            repo = transaction.packages
            repo.insert(package)
            assert len(repo) == 1
            repo.clear()
            assert len(repo) == 0
