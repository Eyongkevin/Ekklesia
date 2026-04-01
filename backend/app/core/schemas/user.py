import uuid
from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    telegram_id: str
    first_name: str | None = None

    # model_config = ConfigDict(from_attributes=True)

class InviteUserCreate(UserBase):
    invite_code: str

class User(UserBase):
    id: uuid.UUID
    church_id: uuid.UUID
    role: str

    model_config = ConfigDict(from_attributes=True)
