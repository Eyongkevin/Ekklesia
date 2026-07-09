from fastapi import APIRouter, Depends

from app.api import deps
from app.services import audience as audience_services
from app.schemas import announcement as announcement_shemas
from app.db.uow import UnitOfWork
from app.models import User

router = APIRouter(prefix="/audience", tags=["audience"])



@router.get("/", response_model=list[announcement_shemas.AnnouncementAudience])
def tags(_: User = Depends(deps.get_user), uow: UnitOfWork = Depends(deps.get_db)):
    return audience_services.AudienceService(uow).get_audiences()
