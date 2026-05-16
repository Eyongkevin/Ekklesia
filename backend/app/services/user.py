from fastapi import HTTPException, status

from app.services.membership import MembershipService
from app.repositories.user import UserCRUD
from app.services.invite import InviteService
from app.models import User
from app.db.uow import UnitOfWork
from app.core.utils import verify_password


class UserService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.user_crud = UserCRUD(self.uow.db)
        self.invite_service = InviteService(self.uow)
        self.membership_service = MembershipService(self.uow)

    def create_user(
        self, 
        telegram_id: str | None = None, 
        first_name: str | None = None, 
        email: str | None = None, 
        password: str | None = None
    ) -> User:
        user = self.user_crud.create_user(telegram_id, first_name, email, password)
        self.uow.commit()
        return user

    def register_user_with_invite(
        self,
        telegram_id: str,
        first_name: str | None,
        code: str
    ) -> User:
        invite = self.invite_service.validate_invite_code(code.strip())
        if not invite:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired invite code")

        # TODO: Check if user already exists
        #   If user exists, raise an error
        user = self.user_crud.get_user_by_telegram_id(telegram_id)
        if user is None:
            user = self.user_crud.create_user(telegram_id, first_name)

        # Check if membership already exists
        if self.membership_service.check_membership(str(user.id), str(invite.church_id)) is False:
            self.membership_service.create_membership(str(user.id), church_id=str(invite.church_id))
            # church_name = user.memberships[0].church.name
            # raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"You already belong to {church_name} church")
        
        self.uow.commit()

        return user

    
    def authenticate_user(self, email: str, password: str) -> User | None:
        user = self.user_crud.get_user_by_email(email)
        if user and verify_password(password, user.password_hash):
            return user
        return None

    def get_user_by_email(self, email: str) -> User | None:
        return self.user_crud.get_user_by_email(email)
    
    def get_user_by_id(self, user_id: str) -> User | None:
        return self.user_crud.get_user_by_id(user_id)
