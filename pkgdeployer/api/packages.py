from uuid import UUID

from fastapi import APIRouter, Query

router = APIRouter(prefix="/packages", tags=["packages"])


@router.get("/")
def get_packages(offset: int = Query(0, ge=0), count: int = Query(50, ge=1, le=100)):
    return {'result': 'get_packages'}


@router.get("/{uuid}")
def get_package(uuid: UUID):
    return {'package': uuid}
