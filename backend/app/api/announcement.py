from fastapi import APIRouter, Depends

from app.api.deps import get_db
from app.services import announcement as service_announcement
from app.core.schemas import announcement as schema_announcement
from app.db.uow import UnitOfWork

router = APIRouter(prefix="/announcements", tags=["announcements"])

@router.post("/")
def create(announcement: schema_announcement.AnnouncementCreate, uow: UnitOfWork = Depends(get_db)) -> schema_announcement.Announcement:
    return service_announcement.AnnouncementService(uow).create(announcement)

# TAGS
@router.get("/tags/")
def tags( uow: UnitOfWork = Depends(get_db)) -> list[schema_announcement.AnnouncementTag]:
    return service_announcement.AnnouncementTagService(uow).get_tags()
