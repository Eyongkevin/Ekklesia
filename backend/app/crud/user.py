from sqlalchemy.orm import Session
from app.models.user import User
from app.core.schemas import user as user_schemas

def get_user_by_telegram_id(db: Session, telegram_id: str) -> user_schemas.User | None:
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    return user_schemas.User.model_validate(user) if user else None

def create_user(db: Session, telegram_id: str, first_name: str | None, church_id: str) -> user_schemas.User:
    new_user = User(
        telegram_id=telegram_id,
        first_name=first_name,
        church_id=church_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return user_schemas.User.model_validate(new_user)