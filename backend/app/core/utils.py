from http.client import HTTPException
from enum import Enum
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.core.schemas.membership import Membership

password_hasher = PasswordHasher()

class MembershipRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    CHURCH_ADMIN = "church_admin"
    MEMBER = "member"
    PRAYER_TEAM = "prayer_team"


def require_role(user: Membership, role: MembershipRole):
    if role != user.role:
        raise HTTPException(status_code=403, detail="Forbidden")
    return user

def verify_password(password: str, hashed: str):
    try:
        password_hasher.verify(hashed, password)
        return True
    except VerifyMismatchError:
        return False

def hash_password(password: str):
    return password_hasher.hash(password)