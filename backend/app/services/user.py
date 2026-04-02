from sqlalchemy.orm import Session
from app.services.membership import check_membership, create_membership
from app.crud.user import get_user_by_telegram_id, create_user
from app.crud.invite import get_active_invite_by_code
from app.core.schemas import user as user_schemas

class UserService:
    @staticmethod
    def register_user_with_invite(
        db: Session,
        telegram_id: str,
        first_name: str | None,
        code: str
    ) -> user_schemas.User:
        invite = get_active_invite_by_code(db, code)
        if not invite:
            raise ValueError("Invalid invite code")

        # TODO: Check if user already exists
        #   If user exists, raise an error
        user = get_user_by_telegram_id(db, telegram_id)
        if user is None:
            user = create_user(db, telegram_id, first_name, str(invite.church_id))

        # Check if membership already exists
        if not check_membership(db, str(user.id), str(invite.church_id)):
            create_membership(db, str(user.id), str(invite.church_id))

        return user
