from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict

from app.schemas.membership import Membership

class UserBase(BaseModel):
    telegram_id: Optional[str] = None
    first_name: Optional[str] = None

    # model_config = ConfigDict(from_attributes=True)

class InviteUserCreate(UserBase):
    telegram_id: str
    invite_code: str # FBCA038-SH8EE8 -> church code - suffix code

class User(UserBase):
    id: uuid.UUID
    memberships: list[Membership]
    password_hash: Optional[str] = None
    email: Optional[str] = None
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)

class UserFirstName(BaseModel):
    first_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str