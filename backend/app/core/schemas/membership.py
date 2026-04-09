import uuid

from pydantic import BaseModel, ConfigDict

from app.core.schemas.church import Church


class MembershipBase(BaseModel):
    church_id: uuid.UUID | None = None
    role: str | None = "member"  # member, prayer_team, admin


class Membership(MembershipBase):
    church: Church | None = None

    model_config = ConfigDict(from_attributes=True)