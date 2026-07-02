from typing import Optional
from datetime import datetime, date
import uuid

from pydantic import BaseModel, ConfigDict, HttpUrl, Field, field_serializer

from app.schemas.user import UserFirstName

# STATUS
class StatusBase(BaseModel):
    name: str
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)

class AnnouncementStatus(StatusBase):
    id: uuid.UUID
    created_at: datetime
    modified_at: datetime

# TAGS
class AnnouncementTagBase(BaseModel):
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)

class AnnouncementTag(AnnouncementTagBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    modified_at: datetime

# AUDIENCE
class AnnouncementAudienceBase(BaseModel):
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)

class AnnouncementAudience(AnnouncementAudienceBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    modified_at: datetime

# ANNOUNCEMENT
class AnnouncementBase(BaseModel):
    title: str
    is_pinned: bool = False
    church_id: uuid.UUID
    created_by: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

class Link(BaseModel):
    title: str
    url: HttpUrl

    @field_serializer("url")
    def serialize_url(self, v):
        return str(v)

class AnnouncementCreate(AnnouncementBase):
    status: str
    content: Optional[str] = None
    links: list[Link] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    audiences: list[str] = Field(default_factory=list)
    publish_at: Optional[date] = None
    expire_at: Optional[date] = None

class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    content: Optional[str] = None
    links: Optional[list[Link]] = None
    is_pinned: Optional[bool] = None
    tags: Optional[list[str]] = None
    audiences: Optional[list[str]] = None
    publish_at: Optional[date] = None
    expire_at: Optional[date] = None


class Announcement(AnnouncementBase):
    id: uuid.UUID
    content: Optional[str] = None
    links: list[Link] = Field(default_factory=list)
    tags: list[AnnouncementTag] = Field(default_factory=list)
    audiences: list[AnnouncementAudience] = Field(default_factory=list)
    status: AnnouncementStatus
    creator: UserFirstName
    publish_at: Optional[date] = None
    expire_at: Optional[date] = None
    created_at: datetime
    modified_at: datetime

class AnnouncementListRes(BaseModel):
    total: int
    announcements: list[Announcement]

class AnnouncementFilterOptions(BaseModel):
    status: str
    audience: str
    tag: str
    search: str
    is_active: bool = True
    page: int = 1
    per_page: int = 10