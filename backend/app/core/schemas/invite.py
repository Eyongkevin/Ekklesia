from typing import Optional
import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class InviteBase(BaseModel):
    expires_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class InviteCreate(InviteBase):
    pass

class Invite(InviteBase):
    id: uuid.UUID
    code: str
    church_id: uuid.UUID
    is_active: bool
    created_at: str
    modified_at: str
