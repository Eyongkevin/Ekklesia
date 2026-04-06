from fastapi import APIRouter, Depends


from app.api.deps import get_db
from app.services.church import ChurchService
from app.core.schemas.church import Church, ChurchCreate
from app.db.uow import UnitOfWork

router = APIRouter(prefix="/churches", tags=["churches"])

@router.post("/")
def create(church: ChurchCreate, uow: UnitOfWork = Depends(get_db)) -> Church:
    return ChurchService(uow).create_church(church.name)

@router.get("/")
def list_churches(uow: UnitOfWork = Depends(get_db)) -> list[Church]:
    return ChurchService(uow).get_churches()