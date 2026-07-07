from http.client import HTTPException
from enum import Enum
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime

from app.schemas.membership import Membership

password_hasher = PasswordHasher()

class MembershipRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    CHURCH_ADMIN = "church_admin"
    MEMBER = "member"
    PRAYER_TEAM = "prayer_team"
    PASTOR = "pastor"
    DEACON = "deacon"
    TEACHER = 'teacher'
    COUNSELOR = 'counselor'

class MemberCategory(str, Enum):
    YOUTH = 'youth'
    ADULT = 'adult'
    ELDER = 'elder'

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

def format_datetime(dt: datetime) -> str:
    if dt is None:
        return "N/A"
    return dt.strftime("%A, %d %B %Y at %I:%M %p")

def format_expire_in(expire_date: datetime | None) -> str:
    if expire_date is None:
        return 'Never'
    
    elif expire_date < datetime.now():
        return '(Expired)'
    
    else:
        time_diff = expire_date - datetime.now()
        seconds = time_diff.total_seconds()
        expire_in = ""

        if seconds >= 86400:
            expire_in = f"{seconds / 86400:.2f} days"
        elif seconds >= 3600:
            expire_in = f"{seconds / 3600:.2f} hours"
        elif seconds >= 60:
            expire_in = f"{seconds / 60:.2f} minutes"
        else:
            expire_in = f"{seconds:.2f} seconds"

        return f"({expire_in})"
        

