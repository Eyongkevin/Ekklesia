import random
import string
from sqlalchemy.orm import Session
from app.crud.invite import create_invite_code

class InviteService:
    @staticmethod
    def generate_code(length: int = 6) -> str:
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    @staticmethod
    def create_invite(db: Session, church_id: str):
        code: str = InviteService.generate_code()
        return create_invite_code(db, code, church_id)

