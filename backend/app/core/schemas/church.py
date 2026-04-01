import uuid
from pydantic import BaseModel, ConfigDict


class ChurchBase(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)

class ChurchCreate(ChurchBase):
    pass

class Church(ChurchBase):
    id: uuid.UUID
