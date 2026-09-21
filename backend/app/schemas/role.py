from typing import Optional
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.schemas.permission import PermissionRes
from app.schemas.membership import Membership

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
    name: str
    is_customized: bool = False
    template_version: Optional[int] = None
    system_role_id: Optional[uuid.UUID] = None
    description: Optional[str] = None
    is_active: bool = True
    is_protected: bool = False

    model_config = ConfigDict(from_attributes=True)

    @field_validator("description", mode="before")
    @classmethod
    def default_empty_string(cls, value):
        return "" if value is None else value

class RoleRes(RoleBase):
    id: uuid.UUID
    created_at: datetime
    modified_at: datetime
    permissions: list[PermissionRes]
    memberships: list[Membership]

class RoleReq(RoleBase):
    permissions: list[str]

class RoleListRes(BaseModel):
    total: int
    roles: list[RoleRes]

class RoleAllRes(BaseModel):
    name: str

class RoleFilterOptions(BaseModel):
    search: str
    from_system: str
    version: str
    active: str
    customized: str
    page: int = 1
    per_page: int = 10

class RoleUpdate(RoleBase):
    permissions: list[str]

class RoleMerge(BaseModel):
    target_role_name: str