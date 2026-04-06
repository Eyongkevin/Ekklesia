from app.services.membership import MembershipService
from app.crud.user import UserCRUD
from app.services.invite import InviteService

from app.core.schemas import user as user_schemas
from app.db.uow import UnitOfWork
from app.core.utils import verify_password


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.user_crud = UserCRUD(self.uow.db)
        self.invite_service = InviteService(self.uow)
        self.membership_service = MembershipService(self.uow)

    def create_user(self, telegram_id: str | None = None, first_name: str | None = None, email: str | None = None, password: str | None = None) -> user_schemas.User:
        return self.user_crud.create_user(telegram_id, first_name, email, password)

    def register_user_with_invite(
        self,
        telegram_id: str,
        first_name: str | None,
        code: str
    ) -> user_schemas.User:
        invite = self.invite_service.validate_invite_code(code)
        if not invite:
            raise ValueError("Invalid invite code")

        # TODO: Check if user already exists
        #   If user exists, raise an error
        user = self.user_crud.get_user_by_telegram_id(telegram_id)
        if user is None:
            user = self.user_crud.create_user(telegram_id, first_name, str(invite.church_id))

        # Check if membership already exists
        if not self.membership_service.check_membership(str(user.id), str(invite.church_id)):
            self.membership_service.create_membership(str(user.id), str(invite.church_id))

        return user
    
    def authenticate_user(self, email: str, password: str) -> user_schemas.User | None:
        user: user_schemas.User | None = self.user_crud.get_user_by_email(email)
        if user and verify_password(password, user.password_hash):
            return user
        return None

    def get_user_by_email(self, email: str) -> user_schemas.User | None:
        return self.user_crud.get_user_by_email(email)
    
    def get_user_by_id(self, user_id: str) -> user_schemas.User | None:
        return self.user_crud.get_user_by_id(user_id)
