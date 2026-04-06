from sqlalchemy.orm import Session
from app.models.user import User
from app.core.schemas import user as user_schemas

class UserCRUD:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_telegram_id(self, telegram_id: str) -> user_schemas.User | None:
        user = self.db.query(User).filter(User.telegram_id == telegram_id).first()
        return user_schemas.User.model_validate(user) if user else None

    def get_user_by_email(self, email: str) -> user_schemas.User | None:
        user = self.db.query(User).filter_by(email=email).first()
        return user_schemas.User.model_validate(user) if user else None
    
    def get_user_by_id(self, user_id: str) -> user_schemas.User | None:
        user = self.db.query(User).filter_by(id=user_id).first()
        return user_schemas.User.model_validate(user) if user else None

    def create_user(self, telegram_id: str | None = None, first_name: str | None = None, email: str | None = None, password: str | None = None) -> user_schemas.User:
        new_user = User(
            telegram_id=telegram_id,
            first_name=first_name,
            email=email,
            password_hash=password
        )
        self.db.add(new_user)
        self.db.flush()
        return user_schemas.User.model_validate(new_user)