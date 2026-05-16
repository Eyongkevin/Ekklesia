from fastapi import Request, HTTPException, status, Depends

from jose import jwt, JWTError

from app.db.uow import UnitOfWork
from app.models import User
from app.core.config import settings
from app.services.user import UserService

def get_db():
    with UnitOfWork() as uow:
        yield uow

def get_user(request: Request, uow: UnitOfWork = Depends(get_db)) -> User:
    token = request.cookies.get('access_token')

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
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

