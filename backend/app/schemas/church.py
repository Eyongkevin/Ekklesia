from typing import Optional

import uuid
from pydantic import BaseModel, ConfigDict

# Theme
class ThemeBase(BaseModel):
    church_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

class ThemeCreate(ThemeBase):
    year: int
    theme: str
    verse: str

class Theme(ThemeCreate):
    id: uuid.UUID

# Church
class ChurchBase(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)

class ChurchCreate(ChurchBase):
    pass

class Church(ChurchBase):
    id: uuid.UUID
    code: str
    themes: list[Theme]

# Church Contact

class ContactBase(BaseModel):
    pass

class ContactCreate(ContactBase):
    church_id: uuid.UUID
    country: Optional[str]
    city: Optional[str]
    address_line: Optional[str]
    phone_1: Optional[str]
    phone_2: Optional[str]
    email: Optional[str]
    facebook: Optional[str]
    youtube: Optional[str]
    instagram: Optional[str]
    website: Optional[str]

    model_config = ConfigDict(from_attributes=True)

class Contact(ContactCreate):
    id: uuid.UUID
