from fastapi import Request, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from app.db.uow import UnitOfWork
from app.models import User
from app.core.config import settings
from app.services.user import UserService

auth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login/")

def get_db():
    with UnitOfWork() as uow:
        yield uow

def get_user(token: str = Depends(auth2_scheme), uow: UnitOfWork = Depends(get_db)) -> User:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is missing."
        )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=settings.ALGORITHM
        )
        user_id = payload.get('sub')

        if not user_id:
            raise JWTError
        
        user = UserService(uow).get_user_by_id(user_id)

        if not user:
            raise JWTError
        
        return user
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

