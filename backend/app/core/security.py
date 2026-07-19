from jose import jwt
import datetime

from app.core.config import settings
from app.core.utils import MembershipRole

ACCESS_TOKEN_EXPIRE_HOURS = 2


def create_access_token(user_id: str) -> str:
    payload: dict[str, str | MembershipRole | datetime.datetime] = {
        "sub": user_id,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token
