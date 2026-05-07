from fastapi import APIRouter, Depends

from app.api.deps import get_db
from app.services import announcement as service_announcement
from app.core.schemas import announcement as schema_announcement
from app.db.uow import UnitOfWork

router = APIRouter(prefix="/announcements", tags=["announcements"])

@router.post("/")
def create(announcement: schema_announcement.AnnouncementCreate, uow: UnitOfWork = Depends(get_db)) -> schema_announcement.Announcement:
    return service_announcement.AnnouncementService(uow).create(announcement)

@router.get("/")
def get_announcements(
    church_id: str,
    status: str | None = None,
    audience: str | None = None,
    tag: str | None = None,
    search: str | None = None,
    is_active: bool = True,
    page: int = 1,
    per_page: int = 10,
    uow: UnitOfWork = Depends(get_db)
) ->  dict[str, list[schema_announcement.Announcement] | int]:
    return service_announcement.AnnouncementService(uow).get_announcements(
        church_id=church_id,
        status=status,
        audience=audience,
        tag=tag,
        search=search,
        is_active=is_active,
        page=page,
        per_page=per_page
    )

# TAGS
@router.get("/tags/")
def tags( uow: UnitOfWork = Depends(get_db)) -> list[schema_announcement.AnnouncementTag]:
    return service_announcement.AnnouncementTagService(uow).get_tags()
