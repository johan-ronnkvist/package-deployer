import pytest
from fastapi.testclient import TestClient

from server.entrypoint import server


@pytest.fixture(scope="module")
def fastapi_client():
    with TestClient(server) as client:
        yield client


class TestServerEndpoints:
    @pytest.mark.usefixtures("restart_server")
    def test_root_endpoint_redirects_to_docs(self, fastapi_client):
        response = fastapi_client.get("/")
        assert response.status_code == 200
        assert response.url.path == "/docs"


class TestPackagesEndpoints:
    def test_packages_endpoint_returns_empty_list(self, fastapi_client):
        response = fastapi_client.get("/packages")
        assert response.status_code == 200
        assert response.json() == []


