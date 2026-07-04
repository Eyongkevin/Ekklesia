from app.repositories.announcement import AnnouncementCRUD, AnnouncementTagCRUD
from app.db.uow import UnitOfWork
from app.schemas import announcement as announcement_schemas
from app.services import audience as audience_services
from app.services import status as status_services
from app.core.exceptions import status as status_exceptions, announcement as announcement_exceptions
from app.models.announcement import AnnouncementStatus, Announcement, AnnouncementTag


# CHURCH
class AnnouncementService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.announcement_crud = AnnouncementCRUD(self.uow.db)

    def create(self, data: announcement_schemas.AnnouncementCreate) -> Announcement:
        # extract tags
        tags = AnnouncementTagService(self.uow).get_tags_by_names(data.tags)
        # extract audience
        audiences = audience_services.AudienceService(self.uow).get_audiences_by_names(data.audiences)
        # extract status
        status: AnnouncementStatus | None = status_services.StatusService(self.uow).get_status_by_name(data.status)
        if not status:
            raise status_exceptions.StatusNotFound("Invalid or missing status when creating announcement")

        dict_data = data.model_dump(exclude_unset=True, exclude=['tags', 'audiences', 'status'])

        announcement = self.announcement_crud.create(
            **dict_data,
            tags=tags,
            audiences=audiences,
            status_id=status.id
        )

        self.uow.commit()

        return announcement
    
    def update(self, announcement_id: str, data: announcement_schemas.AnnouncementUpdate) -> Announcement:
        # First, check if the announcement exists
        existing_announcement: Announcement | None = self.announcement_crud.get_by_id(announcement_id)

        if not existing_announcement:
            raise announcement_exceptions.AnnouncementNotFound("Announcement to be updated not found")

        # Update simple fields
        simple_fields: list[str] = ['title', 'content', 'publish_at', 'expire_at', 'is_pinned']
        for field in simple_fields:
            value = getattr(data, field)
            # if value is not None:
            setattr(existing_announcement, field, value)
        
        # If links are being updated, update them
        if data.links is not None:
            existing_announcement.links = [
                link.model_dump() for link in data.links
            ]

        # If status is being updated, get the new status
        if data.status:
            status = status_services.StatusService(self.uow).get_status_by_name(data.status)
            if not status:
                raise status_exceptions.StatusNotFound("Invalid status when updating announcement")
            existing_announcement.status = status
            if status.name == "Draft":
                existing_announcement.publish_at = None
        
        # If tags are being updated, get the new tags
        if data.tags is not None:
            tags = AnnouncementTagService(self.uow).get_tags_by_names(data.tags)
            existing_announcement.tags = tags

        # If audiences are being updated, get the new audiences
        if data.audiences is not None:
            audiences = audience_services.AudienceService(self.uow).get_audiences_by_names(data.audiences)
            existing_announcement.audiences = audiences
        
        self.uow.commit()

        return existing_announcement
    
    def delete(self, announcement_id: str) -> None:
        announcement = self.announcement_crud.get_by_id(announcement_id)
        if not announcement:
            raise announcement_exceptions.AnnouncementNotFound('Announcement to be deleted not found')
        self.announcement_crud.delete(announcement)

        self.uow.commit()

    def delete_many(self, announcement_ids: list[str]) -> int:
        deleted_ids =  self.announcement_crud.delete_many(announcement_ids)
        if deleted_ids == 0:
            raise announcement_exceptions.AnnouncementDeletionFailed("No announcements were found to delete.")
        
        self.uow.commit()
        return deleted_ids
    
    def get_announcements(
            self,
            church_id: str,
            filters: announcement_schemas.AnnouncementFilterOptions) ->  dict[str, list[Announcement] | int]:
        offset = (filters.page - 1) * filters.per_page

        return self.announcement_crud.get_announcements(
            church_id=church_id,
            status=filters.status,
            audience=None if filters.audience == "All Members" else filters.audience,
            tag=None if filters.tag == "All Tags" else filters.tag,
            search=None if filters.search == "" else filters.search,
            is_active=filters.is_active,
            offset=offset,
            limit=filters.per_page
        )


# TAGS
class AnnouncementTagService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.announcement_tag_crud = AnnouncementTagCRUD(self.uow.db)

    def get_tags(self) -> list[AnnouncementTag]:
        return self.announcement_tag_crud.get_tags()
    
    def get_tags_by_names(self, tag_names: list[str]) -> list[AnnouncementTag]:
        return self.announcement_tag_crud.get_tags_by_names(tag_names)