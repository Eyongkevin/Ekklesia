from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.models.membership import Membership
from app.models.role import Role


class UserCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_telegram_id(self, telegram_id: str) -> User | None:
        return self.db.query(User).filter(User.telegram_id == telegram_id).scalar()

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter_by(email=email).scalar()
    
    def get_user_by_id(self, user_id: str) -> User | None:
        return self.db.query(User).filter_by(id=user_id).scalar()

    def create_user(
        self,
        telegram_id: str | None = None, 
        first_name: str | None = None, 
        email: str | None = None, 
        password: str | None = None
    ) -> User:
        new_user = User(
            telegram_id=telegram_id,
            first_name=first_name,
            email=email,
            password_hash=password
        )
        self.db.add(new_user)

        return new_user

    def get_users_by_role(self, role_id: str) -> list[User]:
        query = (
            select(User)
            .join(User.memberships)
            .join(Membership.roles)
            .where(Role.id == role_id)
            .distinct()
        )
        return self.db.scalars(query).all()

    def has_role(self, user_id: str, role_id: str) -> bool:
        query = (
            select(User)
            .join(User.memberships)
            .join(Membership.roles)
            .where(Role.id == role_id, User.id == user_id)
        ).exists()
        return bool(self.db.scalar(select(query)))

    def assign_role(
        self,
        user_id: str,
        role: Role,
    ) -> Membership:
        membership = self.db.scalar(
            select(Membership)
            .where(Membership.user_id == user_id)
        )

        if not membership:
            raise ValueError("Membership not found")

        if role not in membership.roles:
            membership.roles.append(role)

        self.db.flush()

        return membership
