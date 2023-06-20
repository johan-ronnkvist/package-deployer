import uuid

import pytest

from pkgdeployer.domain.package import Package
from pkgdeployer.repository.abstract_repository import Repository
from pkgdeployer.repository.memory_repository import MemoryRepository


@pytest.fixture()
def package():
    return Package(uuid.uuid4(), 'test_package')


@pytest.mark.parametrize('repository', [MemoryRepository])
class TestRepository:
    def test_initialize(self, repository):
        repo = repository()
        assert isinstance(repo, Repository)

    def test_insert_success(self, repository, package):
        repo = repository()
        assert len(repo) == 0
        assert package not in repo
        repo.insert(package)
        assert len(repo) == 1
        assert package in repo

    def test_insert_duplicate(self, repository, package):
        repo = repository()
        repo.insert(package)
        with pytest.raises(KeyError):
            repo.insert(package)

    def test_find_success(self, repository, package):
        repo = repository()
        repo.insert(package)
        result = repo.find(package.uuid)
        assert result is not None
        assert result == package

    def test_find_failure(self, repository, package):
        repo = repository()
        invalid_uuid = uuid.uuid4()
        result = repo.find(invalid_uuid)
        assert result is None

    def test_remove_successful(self, repository, package):
        repo = repository()
        repo.insert(package)
        assert package in repo
        repo.delete(package.uuid)
        assert package not in repo

    def test_remove_failure(self, repository, package):
        repo = repository()
        with pytest.raises(KeyError):
            repo.delete(package.uuid)

    def test_clear(self, repository, package):
        repo = repository()
        repo.insert(package)
        assert len(repo) == 1
        repo.clear()
        assert len(repo) == 0
