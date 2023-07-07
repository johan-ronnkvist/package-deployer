from uuid import uuid4, UUID

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from pkgdeployer.domain.package import Package
from pkgdeployer.domain.commands import CreatePackageCommand
from pkgdeployer.services.ioc_container import IoCContainer
from pkgdeployer.services.messaging import MessageBus
from pkgdeployer.domain.queries import ListPackagesQuery, FindPackageQuery


def root_endpoints() -> APIRouter:
    router = APIRouter(tags=["root"])

    @router.get("/")
    def root():
        return RedirectResponse(url="/docs")

    return router


def packages_endpoints(container: IoCContainer) -> APIRouter:
    router = APIRouter(prefix="/packages", tags=["packages"])

    class PackageResponse(BaseModel):
        uuid: UUID
        name: str

        @classmethod
        def from_orm(cls, package: Package):
            return cls(uuid=package.uuid, name=package.name)

    class PackagesListResponse(BaseModel):
        result: list[PackageResponse]

    class PackageCreateRequest(BaseModel):
        name: str

    @router.get("/", response_model=PackagesListResponse)
    def get_packages(offset: int = Query(0, ge=0), count: int = Query(50, ge=1, le=100)):
        try:
            messagebus = container.resolve(MessageBus)
            result = messagebus.publish(ListPackagesQuery(offset=offset, count=count))
            return PackagesListResponse(result=[PackageResponse.from_orm(package) for package in result.packages])
        except Exception as error:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {error}")

    @router.post("/", response_model=PackageResponse)
    def create_package(request: PackageCreateRequest):
        try:
            messagebus = container.resolve(MessageBus)
            package_uuid = uuid4()
            messagebus.publish(CreatePackageCommand(package_uuid, request.name))
            return PackageResponse(uuid=package_uuid, name=request.name)
        except Exception as error:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {error}")

    @router.get("/{uuid}", response_model=PackageResponse)
    def get_package(uuid: UUID):
        try:
            messagebus = container.resolve(MessageBus)
            result = messagebus.publish(FindPackageQuery(uuid=uuid))
            return PackageResponse.from_orm(result.package)
        except Exception as error:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {error}")

    return router
