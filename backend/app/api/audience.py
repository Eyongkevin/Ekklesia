from fastapi import APIRouter, Depends

from app.api.deps import get_db
from app.services import audience as audience_service
from app.core.schemas import announcement as schema_announcement
from app.db.uow import UnitOfWork

router = APIRouter(prefix="/audience", tags=["audience"])


@router.get("/")
def tags( uow: UnitOfWork = Depends(get_db)) -> list[schema_announcement.AnnouncementAudience]:
    return audience_service.AudienceService(uow).get_audiences()
