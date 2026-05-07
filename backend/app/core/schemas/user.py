import uuid
from pydantic import BaseModel, ConfigDict

from app.core.schemas.membership import Membership

class UserBase(BaseModel):
    telegram_id: str | None = None
    first_name: str | None = None

    # model_config = ConfigDict(from_attributes=True)

class InviteUserCreate(UserBase):
    invite_code: str

class User(UserBase):
    id: uuid.UUID
    memberships: list[Membership]
    password_hash: str | None = None
    email: str | None = None
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)

class UserAnnouncement(BaseModel):
    first_name: str | None = None

    model_config = ConfigDict(from_attributes=True)
class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    message: str
    user: User