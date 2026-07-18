from typing import Optional

from pydantic import BaseModel, ConfigDict

# Theme
class PermissionBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool = True

    model_config = ConfigDict(frozen=True)

class PermissionRes(PermissionBase):
    model_config = ConfigDict(from_attributes=True)

class PermissionReq(PermissionBase):
    pass
