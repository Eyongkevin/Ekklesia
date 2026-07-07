from sqlalchemy.orm import Session
from app.models.announcement import AnnouncementAudience
from app.schemas import announcement as schema_announcement

class AudienceCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_audiences(self) -> list[AnnouncementAudience]:
        return self.db.query(AnnouncementAudience).filter_by(is_active = True).all()

    def get_audiences_by_names(self, audience_names: list[str]) -> list[AnnouncementAudience]:
        return self.db.query(AnnouncementAudience).filter(AnnouncementAudience.name.in_(audience_names)).all()
