from app.repositories.church import ChurchCRUD, ContactCRUD, ThemeCRUD
from app.db.uow import UnitOfWork
from app.schemas import church as schema_church
from app.services.membership import MembershipService
from app.models.church import ChurchContact, ChurchTheme, Church


# CHURCH
class ChurchService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.church_crud = ChurchCRUD(self.uow.db)

    def create_church(self, name: str) -> Church:
        church = self.church_crud.create_church(name)
        self.uow.commit()
        return church
    
    def get_church_by_id(self, church_id: str) -> Church | None:
        return self.church_crud.get_church_by_id(church_id)

    def get_churches(self) -> list[Church]:
        return self.church_crud.get_churches()
    
    def get_church_code(self, church_id: str) -> str:
        return self.church_crud.get_church_code(church_id)
    
    def get_church_by_user_id(self, user_id: str) -> Church | None:
        membership = MembershipService(self.uow).user_church_membership(user_id)
        if membership:
            return self.get_church_by_id(str(membership.church_id))

# CONTACT

class ChurchContactService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.contact_crud = ContactCRUD(self.uow.db)

    def create_or_update_contact(self, contact: schema_church.ContactCreate) -> ChurchContact | None:
        church_contact = self.contact_crud.create_or_update_contact(contact)
        self.uow.commit()
        return church_contact
    
    def get_church_contact_by_church_id(self, church_id: str) -> ChurchContact | None:
        return self.contact_crud.get_contact_by_church_id(church_id)
    
# THEME
class ChurchThemeService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.theme_crud = ThemeCRUD(self.uow.db)

    def create_or_update_theme(self, theme: schema_church.ThemeCreate) -> ChurchTheme| None:
        church_theme = self.theme_crud.create_or_update_theme(theme)
        self.uow.commit()
        return church_theme
    
    def get_theme_by_church_id_and_year(self, church_id: str, year: int) -> ChurchTheme | None:
        return self.theme_crud.get_theme_by_church_id_and_year(church_id, year)