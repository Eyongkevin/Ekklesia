from fastapi import APIRouter, Depends

from app.api.deps import get_db
from app.services import status as status_service
from app.core.schemas import announcement as schema_announcement
from app.db.uow import UnitOfWork

router = APIRouter(prefix="/status", tags=["status"])


@router.get("/")
def tags( uow: UnitOfWork = Depends(get_db)) -> list[schema_announcement.AnnouncementStatus]:
    return status_service.StatusService(uow).get_statuses()
