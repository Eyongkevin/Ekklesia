from app.crud.announcement import AnnouncementCRUD, AnnouncementTagCRUD
from app.db.uow import UnitOfWork
from app.core.schemas import announcement as schema_announcement
from app.services import audience as audience_service
from app.services import status as status_service
from app.models.announcement import AnnouncementStatus


# CHURCH
class AnnouncementService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.announcement_crud = AnnouncementCRUD(self.uow.db)

    def create(self, data: schema_announcement.AnnouncementCreate) -> schema_announcement.Announcement:
        # todo: extract tags
        tags = AnnouncementTagService(self.uow).get_tags_by_names(data.tags)
        # todo: extract audience
        audiences = audience_service.AudienceService(self.uow).get_audiences_by_names(data.audiences)
        # todo: extract status
        status: AnnouncementStatus = status_service.StatusService(self.uow).get_status_by_name(data.status)

        dict_data = data.model_dump(exclude_unset=True, exclude=['tags', 'audiences', 'status'])

        return self.announcement_crud.create(
            **dict_data,
            tags=tags,
            audiences=audiences,
            status_id=status.id
        )
    

# TAGS
class AnnouncementTagService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.announcement_tag_crud = AnnouncementTagCRUD(self.uow.db)

    def get_tags(self):
        return self.announcement_tag_crud.get_tags()
    
    def get_tags_by_names(self, tag_names: list[str]):
        return self.announcement_tag_crud.get_tags_by_names(tag_names)