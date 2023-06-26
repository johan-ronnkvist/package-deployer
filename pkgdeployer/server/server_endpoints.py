from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import RedirectResponse

from pkgdeployer.services.ioc_container import IoCContainer
from pkgdeployer.services.messaging import MessageBus
from pkgdeployer.domain.queries import ListPackagesQuery


def root_endpoints() -> APIRouter:
    router = APIRouter(tags=["root"])

    @router.get("/")
    def root():
        return RedirectResponse(url="/docs")

    return router


def packages_endpoints(container: IoCContainer) -> APIRouter:
    router = APIRouter(prefix="/packages", tags=["packages"])

    @router.get("/")
    def get_packages(offset: int = Query(0, ge=0), count: int = Query(50, ge=1, le=100)):
        try:
            messagebus = container.resolve(MessageBus)
            result = messagebus.publish(ListPackagesQuery(offset=offset, count=count))
        except Exception as error:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {error}")
        return {'result': 'get_packages'}

    @router.post("/")
    def create_package():
        return {'result': 'create_package'}

    return router
