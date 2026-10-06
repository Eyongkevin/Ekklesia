from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict
from app.core.utils import UserCreationSource
from app.schemas import membership_base as membership_base_schemas
from datetime import datetime


class UserBase(BaseModel):
    telegram_id: Optional[str] = None
    first_name: Optional[str] = None

class UserAdmin(BaseModel):
    id: uuid.UUID
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    created_by: Optional["UserAdmin"] = None
    creation_source: UserCreationSource
    memberships: list[membership_base_schemas.Membership]
    created_at: datetime
    modified_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserAdminListRes(BaseModel):
    total: int
    admins: list[UserAdmin]
