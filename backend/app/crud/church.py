from typing import Optional
from datetime import date

from sqlalchemy.orm import Session, selectinload, with_loader_criteria
from app.models.church import Church, ChurchContact, ChurchTheme
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
        church = self.db.query(Church).options(selectinload(Church.themes), with_loader_criteria(ChurchTheme, ChurchTheme.year == date.today().year)).filter(Church.id == church_id).first()
        return church_schema.Church.model_validate(church) if church else None
    
    def get_church_code(self, church_id: str) -> str | None:
        return self.db.query(Church.code).filter(Church.id==church_id).scalar()

    def get_churches(self):
        return self.db.query(Church).all()

# CONTACT
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

# THEME
class ThemeCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_or_update_theme(self, theme: church_schema.ThemeCreate) -> church_schema.Theme | None:
        church_theme: Optional[ChurchTheme] = self.get_theme_by_church_id_and_year(str(theme.church_id), theme.year)

        theme_dict = theme.model_dump(exclude_unset=True)
        theme_dict.pop("church_id", None)

        if not church_theme:
            church_theme = ChurchTheme(
                church_id = theme.church_id,
                **theme_dict
            )
            self.db.add(church_theme)
        else:
            for key, value in theme_dict.items():
                setattr(church_theme, key, value)

        self.db.commit()
        self.db.refresh(church_theme)
        return church_schema.Theme.model_validate(church_theme) if church_theme else None

    def get_theme_by_church_id_and_year(self, church_id: str, year: int) -> Optional[ChurchTheme]:
        theme = self.db.query(ChurchTheme).filter(ChurchTheme.church_id == church_id, ChurchTheme.year == year).first()
        if theme and church_schema.Theme.model_validate(theme):
            return theme
