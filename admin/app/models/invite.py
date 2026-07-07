from typing import Optional

from pydantic import BaseModel

class InviteCodeBase(BaseModel):
    code: str
    expires_at: Optional[str]
    is_active: bool = True

class InviteCodeRes(InviteCodeBase):
    id: str
    expire_in: str
    created: str
    created_by: str