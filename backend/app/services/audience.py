from app.crud.audience import AudienceCRUD
from app.db.uow import UnitOfWork
from app.core.schemas import announcement as schema_announcement


class AudienceService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.audience_crud = AudienceCRUD(self.uow.db)

    def get_audiences(self)-> list[schema_announcement.AnnouncementAudience]:
        return self.audience_crud.get_audiences()
    
    def get_audiences_by_names(self, audience_names: list[str]):
        return self.audience_crud.get_audiences_by_names(audience_names)