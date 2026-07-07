from fastapi import APIRouter, Depends, status as http_status

from app.api.deps import get_db
from app.services import announcement as announcement_services
from app.schemas import announcement as announcement_schemas
from app.db.uow import UnitOfWork

router = APIRouter(prefix="/announcements", tags=["announcements"])

@router.post("/", response_model=announcement_schemas.Announcement)
def create(announcement: announcement_schemas.AnnouncementCreate, uow: UnitOfWork = Depends(get_db)):
    return announcement_services.AnnouncementService(uow).create(announcement)


@router.put("/{announcement_id}/", response_model=announcement_schemas.Announcement)
def update(announcement_id: str, announcement: announcement_schemas.AnnouncementUpdate, uow: UnitOfWork = Depends(get_db)):
    return announcement_services.AnnouncementService(uow).update(announcement_id, announcement)


@router.delete("/{announcement_id}/", status_code=http_status.HTTP_204_NO_CONTENT)
def delete(announcement_id: str, uow: UnitOfWork = Depends(get_db)) -> None:
    return announcement_services.AnnouncementService(uow).delete(announcement_id)


@router.get("/", response_model=announcement_schemas.AnnouncementListRes)
def get_announcements(
    church_id: str,
    filters: announcement_schemas.AnnouncementFilterOptions = Depends(),
    uow: UnitOfWork = Depends(get_db)):
        return announcement_services.AnnouncementService(uow).get_announcements(church_id, filters)


# TAGS
@router.get("/tags/", response_model=list[announcement_schemas.AnnouncementTag])
def tags( uow: UnitOfWork = Depends(get_db)):
    return announcement_services.AnnouncementTagService(uow).get_tags()
