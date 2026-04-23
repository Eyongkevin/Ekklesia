from typing import Optional

from sqlalchemy.orm import Session
from app.models.church import Church, ChurchContact
from app.core.schemas import church as church_schema


class ChurchCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_church(self, name: str):
        church = Church(
            name=name
        )
        self.db.add(church)
        self.db.commit()
        self.db.refresh(church)
        return church

    def get_church_by_id(self, church_id: str):
        church = self.db.query(Church).filter(Church.id == church_id).first()
        return church_schema.Church.model_validate(church) if church else None

    def get_churches(self):
        return self.db.query(Church).all()

class ContactCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_or_update_contact(self, contact: church_schema.ContactCreate) -> church_schema.Contact | None:
        church_contact = self.get_contact_by_church_id(str(contact.church_id))

        contact_dict = contact.model_dump(exclude_unset=True)
        contact_dict.pop("church_id", None)

        if not church_contact:
            church_contact = ChurchContact(
                church_id = contact.church_id,
                **contact_dict
            )
            self.db.add(church_contact)
        else:
            for key, value in contact_dict.items():
                setattr(church_contact, key, value)

        self.db.commit()
        self.db.refresh(church_contact)
        return church_schema.Contact.model_validate(church_contact) if church_contact else None
    
    def get_contact_by_church_id(self, church_id: str) -> Optional[ChurchContact]:
        contact = self.db.query(ChurchContact).filter(ChurchContact.church_id == church_id).first()
        if contact and church_schema.Contact.model_validate(contact):
            return contact
