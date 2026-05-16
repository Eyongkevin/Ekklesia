from fastapi import APIRouter, Depends

from app.api.deps import get_db
from app.services import status as status_services
from app.schemas import announcement as announcement_schemas
from app.db.uow import UnitOfWork


router = APIRouter(prefix="/status", tags=["status"])



@router.get("/", response_model=list[announcement_schemas.AnnouncementStatus])
def tags(uow: UnitOfWork = Depends(get_db)):
    return status_services.StatusService(uow).get_statuses()
