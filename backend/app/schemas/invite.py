from typing import Optional
import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, HttpUrl, computed_field

from app.schemas.user import UserFirstName
from app.core.utils import format_expire_in


class InviteBase(BaseModel):
    # TODO: Move 'code' to base and add verification
    expires_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class InviteCreate(InviteBase):
    code: str
    state: bool

class InviteUpdate(InviteBase):
    is_active: Optional[bool] = None

class Invite(InviteBase):
    id: uuid.UUID
    code: str
    church_id: uuid.UUID
    creator: UserFirstName
    is_active: bool
    created_at: datetime
    modified_at: datetime

    @computed_field
    @property
    def expire_in(self) -> str:
        return format_expire_in(self.expires_at)

class InviteRes(BaseModel):
    code: str
    link: HttpUrl

class InviteFilterOptions(BaseModel):
    state: Optional[str] = None
    is_active: Optional[bool] = None
    page: int = 1
    per_page: int = 10

class InvitetListRes(BaseModel):
    total: int
    invites: list[Invite]
