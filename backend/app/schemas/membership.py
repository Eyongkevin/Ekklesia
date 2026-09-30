import uuid

from pydantic import BaseModel, ConfigDict

from app.schemas.church import Church
from app.schemas.user import User
from app.schemas import role_base as role_schemas


class MembershipBase(BaseModel):
    church_id: uuid.UUID | None = None
    role: str | None = "member"  # member, prayer_team, admin


class Membership(MembershipBase):
    
    church: Church | None = None
    user: User
    roles: list[role_schemas.RoleAllRes]

    model_config = ConfigDict(from_attributes=True)