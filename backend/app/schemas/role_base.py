import uuid
from pydantic import BaseModel


class RoleAllRes(BaseModel):
    id: uuid.UUID
    name: str