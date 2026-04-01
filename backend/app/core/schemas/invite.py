import uuid
from pydantic import BaseModel, ConfigDict

class InviteBase(BaseModel):
    church_id: str

    model_config = ConfigDict(from_attributes=True)

class InviteCreate(InviteBase):
    pass

class Invite(InviteBase):
    id: uuid.UUID
    code: str
    church_id: uuid.UUID
    is_active: bool
    expires_at: str | None
    created_at: str
    modified_at: str
