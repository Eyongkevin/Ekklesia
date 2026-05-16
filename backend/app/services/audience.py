from app.repositories.audience import AudienceCRUD
from app.db.uow import UnitOfWork
from app.models import AnnouncementAudience


class AudienceService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.audience_crud = AudienceCRUD(self.uow.db)

    def get_audiences(self)-> list[AnnouncementAudience]:
        return self.audience_crud.get_audiences()
    
    def get_audiences_by_names(self, audience_names: list[str]) -> list[AnnouncementAudience]:
        return self.audience_crud.get_audiences_by_names(audience_names)