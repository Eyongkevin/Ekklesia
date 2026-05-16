from fastapi import APIRouter, Depends

from app.api.deps import get_db
from app.services import audience as audience_services
from app.schemas import announcement as announcement_shemas
from app.db.uow import UnitOfWork

router = APIRouter(prefix="/audience", tags=["audience"])



@router.get("/", response_model=list[announcement_shemas.AnnouncementAudience])
def tags(uow: UnitOfWork = Depends(get_db)):
    return audience_services.AudienceService(uow).get_audiences()
