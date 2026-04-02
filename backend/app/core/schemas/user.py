import uuid
from pydantic import BaseModel, ConfigDict

from app.core.schemas.membership import Membership

class UserBase(BaseModel):
    telegram_id: str
    first_name: str | None = None

    # model_config = ConfigDict(from_attributes=True)

class InviteUserCreate(UserBase):
    invite_code: str

class User(UserBase):
    id: uuid.UUID
    memberships: list[Membership]

    model_config = ConfigDict(from_attributes=True)
