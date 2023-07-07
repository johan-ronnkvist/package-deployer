import logging

import uvicorn
import fastapi

from pkgdeployer.server.endpoints import packages_endpoints, root_endpoints
from pkgdeployer.server.bootstrap import bootstrap

logging.root.setLevel(logging.DEBUG)
_logger = logging.getLogger(__name__)

server = fastapi.FastAPI()
container = bootstrap()


@server.on_event("startup")
async def startup_event():
    _logger.info("Starting up server")


@server.on_event("shutdown")
async def shutdown_event():
    _logger.info("Shutting down server")


server.include_router(root_endpoints())
server.include_router(packages_endpoints(container))


if __name__ == '__main__':
    uvicorn.run("entrypoint:server", host="localhost", port=8000, reload=True)
