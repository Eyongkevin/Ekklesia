from sqlalchemy.orm import Session
from app.models.announcement import AnnouncementAudience
from app.core.schemas import announcement as schema_announcement

class AudienceCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_audiences(self) -> list[schema_announcement.AnnouncementAudience]:
        audiences = self.db.query(AnnouncementAudience).filter(AnnouncementAudience.is_active == True).all()
        return [schema_announcement.AnnouncementAudience.model_validate(audience) for audience in audiences]
    
    def get_audiences_by_names(self, audience_names: list[str]) -> list[AnnouncementAudience]:
        return self.db.query(AnnouncementAudience).filter(AnnouncementAudience.name.in_(audience_names)).all()
