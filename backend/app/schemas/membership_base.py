from pydantic import BaseModel, ConfigDict

from app.schemas import role_base as role_schemas


class Membership(BaseModel):
    roles: list[role_schemas.RoleAllRes]

    model_config = ConfigDict(from_attributes=True)