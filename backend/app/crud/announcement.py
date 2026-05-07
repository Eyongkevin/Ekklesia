from typing import Optional
from datetime import datetime
import uuid

from sqlalchemy.orm import Session
from app.models.announcement import Announcement, AnnouncementTag, AnnouncementAudience, AnnouncementStatus
from app.core.schemas import announcement as schema_announcement


class AnnouncementCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create(
            self,
            title: str,
            status_id: uuid.UUID,
            created_by: uuid.UUID,
            church_id: uuid.UUID,
            is_pinned: bool = False,
            tags: Optional[list[AnnouncementTag]] = None,
            audiences: Optional[list[AnnouncementAudience]] = None,
            publish_at: Optional[datetime] = None,
            expire_at: Optional[datetime] = None,
            content: Optional[str] = None,
            links: Optional[list[schema_announcement.Link]] = None,
    ) -> schema_announcement.Announcement:
        announcement = Announcement(
            title=title,
            content=content,
            links=links,
            status_id=status_id,
            is_pinned=is_pinned,
            publish_at=publish_at,
            expire_at=expire_at,
            created_by=created_by,
            church_id=church_id,
            tags=tags,
            audiences=audiences
        )
        self.db.add(announcement)
        self.db.commit()
        self.db.refresh(announcement)
        return schema_announcement.Announcement.model_validate(announcement)
    
    def get_announcements(self, 
                    church_id: str,
                    status: str | None = None,
                    audience: str | None = None,
                    tag: str | None = None,
                    search: str | None = None,
                    is_active: bool = True,
                    offset: int = 0,
                    limit: int = 10) -> dict[str, list[schema_announcement.Announcement] | int]:
        # TODO: optimize query by limiting with is_active
        query = self.db.query(Announcement).filter(Announcement.church_id == church_id)
        if status:
            query = query.join(Announcement.status).filter(AnnouncementStatus.name == status)
        if audience:
            query = query.join(Announcement.audiences).filter(AnnouncementAudience.name == audience)
        if tag:
            query = query.join(Announcement.tags).filter(AnnouncementTag.name == tag)
        if search:
            query = query.filter(Announcement.title.ilike(f'%{search}%'))

        total = query.count()

        announcements = query.order_by(Announcement.created_at.desc()).offset(offset).limit(limit).all()
        return {
            "announcements": [schema_announcement.Announcement.model_validate(announcement) for announcement in announcements],
            "total": total
        }

class AnnouncementTagCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_tags(self) -> list[schema_announcement.AnnouncementTag]:
        tags = self.db.query(AnnouncementTag).filter(AnnouncementTag.is_active == True).all()
        return [schema_announcement.AnnouncementTag.model_validate(tag) for tag in tags]
    
    def get_tags_by_names(self, tag_names: list[str]) -> list[AnnouncementTag]:
        return self.db.query(AnnouncementTag).filter(AnnouncementTag.name.in_(tag_names)).all()


