from fastapi import APIRouter, Query

from pkgdeployer.services.ioc_container import IoCContainer
from pkgdeployer.services.messaging import MessageBus
from pkgdeployer.domain.queries import ListPackagesQuery


def packages_router(container: IoCContainer) -> APIRouter:
    router = APIRouter(prefix="/packages", tags=["packages"])

    @router.get("/")
    def get_packages(offset: int = Query(0, ge=0), count: int = Query(50, ge=1, le=100)):
        messagebus = container.resolve(MessageBus)
        messagebus.publish(ListPackagesQuery(offset=offset, count=count))
        return {'result': 'get_packages'}

    @router.post("/")
    def create_package():
        return {'result': 'create_package'}

    return router
