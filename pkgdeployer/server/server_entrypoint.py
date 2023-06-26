import logging
import threading

import uvicorn
import fastapi

from pkgdeployer.domain.queries import ListPackagesQuery, list_packages
from pkgdeployer.server.server_endpoints import packages_endpoints, root_endpoints
from pkgdeployer.server.server_config import bootstrap
from pkgdeployer.services.messaging import MessageBus

logging.root.setLevel(logging.DEBUG)
_logger = logging.getLogger(__name__)

app = fastapi.FastAPI()
container = bootstrap()


@app.on_event("startup")
async def startup_event():
    _logger.info("Starting up server")


@app.on_event("shutdown")
async def shutdown_event():
    _logger.info("Shutting down server")


app.include_router(root_endpoints())
app.include_router(packages_endpoints(container))


if __name__ == '__main__':
    uvicorn.run("server_entrypoint:app", host="localhost", port=8000, reload=True)
