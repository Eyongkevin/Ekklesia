from typing import Optional
from sqlalchemy.orm import Session
from app.models.announcement import AnnouncementStatus
from app.core.schemas import announcement as schema_announcement

    
class StatusCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_statuses(self) -> list[schema_announcement.AnnouncementStatus]:
        tags = self.db.query(AnnouncementStatus).filter(AnnouncementStatus.is_active == True).all()
        return [schema_announcement.AnnouncementStatus.model_validate(tag) for tag in tags]
    
    def get_status_by_name(self, status_name: list[str]) -> Optional[AnnouncementStatus]:
        return self.db.query(AnnouncementStatus).filter(AnnouncementStatus.name == status_name).first()

