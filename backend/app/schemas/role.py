from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict

from app.schemas.permission import PermissionRes

# Theme
class SystemRoleBase(BaseModel):
    name: str
    version: int = 1
    description: Optional[str] = None
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)

class SystemRoleRes(SystemRoleBase):
    id: uuid.UUID
    permissions: list[PermissionRes]

class SystemRoleReq(SystemRoleBase):
    permissions: list[str]
