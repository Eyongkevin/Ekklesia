from pydantic import BaseModel, ConfigDict

from app.core.schemas.church import Church


class MembershipBase(BaseModel):
    role: str | None = "member"  # member, prayer_team, admin


class Membership(MembershipBase):
    church: Church

    model_config = ConfigDict(from_attributes=True)