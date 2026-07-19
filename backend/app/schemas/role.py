from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict

from app.schemas.permission import PermissionRes

# System Role
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

# Role
class RoleBase(BaseModel):
    church_id: uuid.UUID
    name: str
    is_customized: bool
    template_version: int
    system_role_id: Optional[uuid.UUID] = None
    description: Optional[str] = None
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)

class RoleRes(RoleBase):
    id: uuid.UUID
    permissions: list[PermissionRes]

class RoleReq(RoleBase):
    permissions: list[str]
