from typing import Optional
from sqlalchemy.orm import Session
from app.models.announcement import AnnouncementStatus

    
class StatusCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_statuses(self) -> list[AnnouncementStatus]:
        return self.db.query(AnnouncementStatus).filter_by(is_active = True).all()
    
    def get_status_by_name(self, status_name: str) -> Optional[AnnouncementStatus]:
        return self.db.query(AnnouncementStatus).filter(AnnouncementStatus.name == status_name).scalar()

