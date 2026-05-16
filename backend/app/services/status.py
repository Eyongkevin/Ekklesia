from app.repositories.status import StatusCRUD
from app.db.uow import UnitOfWork
from app.models import AnnouncementStatus


class StatusService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.status_crud = StatusCRUD(self.uow.db)

    def get_statuses(self)-> list[AnnouncementStatus]:
        return self.status_crud.get_statuses()
    
    def get_status_by_name(self, status_name: str)-> AnnouncementStatus | None:
        return self.status_crud.get_status_by_name(status_name)