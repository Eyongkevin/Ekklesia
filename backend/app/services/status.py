from app.crud.status import StatusCRUD
from app.db.uow import UnitOfWork
from app.core.schemas import announcement as schema_announcement


class StatusService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.status_crud = StatusCRUD(self.uow.db)

    def get_statuses(self)-> list[schema_announcement.AnnouncementStatus]:
        return self.status_crud.get_statuses()
    
    def get_status_by_name(self, status_name: list[str]):
        return self.status_crud.get_status_by_name(status_name)