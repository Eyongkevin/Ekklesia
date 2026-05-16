from sqlalchemy.orm import Session
from app.models.user import User


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