from typing import Optional
from datetime import date

from sqlalchemy.orm import Session, selectinload, with_loader_criteria
from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound, NoResultFound, IntegrityError
from app.models.church import Church, ChurchContact, ChurchTheme
from app.schemas import church as church_schema
from app.core.exceptions import church as church_exceptions


class ChurchCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_church(self, name: str):
        church = Church(
            name=name
        )
        self.db.add(church)

        try:
            self.db.flush()
        except IntegrityError as exc:
            raise church_exceptions.ChurchConstraintViolationError() from exc

        return church

    def get_church_by_id(self, church_id: str) -> Church | None:
        return self.db.query(Church).options(selectinload(Church.themes), with_loader_criteria(ChurchTheme, ChurchTheme.year == date.today().year)).filter(Church.id == church_id).scalar()


    def get_church_code(self, church_id: str) -> str:
        query = select(Church.code).where(Church.id==church_id)
        try:
            church_code = self.db.execute(query)
            return church_code.scalar_one()
        except NoResultFound as exc:
            raise church_exceptions.NoChurchCodeFound() from exc



    def get_churches(self):
        return self.db.query(Church).all()

# CONTACT
class ContactCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_or_update_contact(self, contact: church_schema.ContactCreate) -> ChurchContact | None:
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

        return church_contact
    
    def get_contact_by_church_id(self, church_id: str) -> Optional[ChurchContact]:
        return self.db.query(ChurchContact).filter(ChurchContact.church_id == church_id).scalar()

# THEME
class ThemeCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create_or_update_theme(self, theme: church_schema.ThemeCreate) -> ChurchTheme | None:
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

        return church_theme

    def get_theme_by_church_id_and_year(self, church_id: str, year: int) -> Optional[ChurchTheme]:
        query = select(ChurchTheme).where(
            ChurchTheme.church_id == church_id,
            ChurchTheme.year == year
        )
        try:
            theme = self.db.execute(query)
            return theme.scalar_one_or_none()
        except MultipleResultsFound as exc:
            raise church_exceptions.DuplicateChurchThemeForYear() from exc
