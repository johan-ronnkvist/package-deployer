import logging
import os

import uvicorn
import fastapi
from fastapi.responses import RedirectResponse

from pkgdeployer.bootstrap import bootstrap
from pkgdeployer.domain.queries import ListPackagesQuery, list_packages
from pkgdeployer.entrypoints.server_packages_api import packages_router
from pkgdeployer.services.messaging import MessageBus

logging.root.setLevel(logging.DEBUG)
_logger = logging.getLogger(__name__)

app = fastapi.FastAPI()

container = bootstrap()


@app.on_event("startup")
async def startup_event():
    _logger.info("Starting up server")
    messagebus = container.resolve(MessageBus)
    initialize_handlers(messagebus)


@app.on_event("shutdown")
async def shutdown_event():
    _logger.info("Shutting down server")


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health():
    return {'result': 'ok'}


app.include_router(packages_router(container))


def initialize_handlers(messagebus: MessageBus):
    messagebus.register_handler(ListPackagesQuery, list_packages)


if __name__ == '__main__':
    uvicorn.run("server:app", host="localhost", port=8000, reload=True)
