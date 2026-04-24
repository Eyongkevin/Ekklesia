from typing import Optional

from fastapi import APIRouter, Depends


from app.api.deps import get_db
from app.services import church as church_service
from app.core.schemas import church as schema_church
from app.db.uow import UnitOfWork

router = APIRouter(prefix="/churches", tags=["churches_contacts_theme"])

@router.post("/")
def create(church: schema_church.ChurchCreate, uow: UnitOfWork = Depends(get_db)) -> schema_church.Church:
    return church_service.ChurchService(uow).create_church(church.name)

@router.get("/")
def list_churches(uow: UnitOfWork = Depends(get_db)) -> list[schema_church.Church]:
    return church_service.ChurchService(uow).get_churches()

@router.get('/{church_id}')
def get_church(church_id: str, uow: UnitOfWork = Depends(get_db)) -> Optional[schema_church.Church]:
    return church_service.ChurchService(uow).get_church_by_id(church_id)

@router.get('/user/{user_id}')
def get_user_church(user_id: str, uow: UnitOfWork = Depends(get_db)) -> Optional[schema_church.Church]:
    return church_service.ChurchService(uow).get_church_by_user_id(user_id)

# CONTACT

@router.post('/contact/')
def create_or_update_contact(contact: schema_church.ContactCreate, uow: UnitOfWork = Depends(get_db)) -> Optional[schema_church.Contact]:
    return church_service.ChurchContactService(uow).create_or_update_contact(contact) 

@router.get('/contact/{church_id}')
def get_church_contact(church_id: str, uow: UnitOfWork = Depends(get_db)):
    return church_service.ChurchContactService(uow).get_church_contact_by_church_id(church_id)

# THEME
@router.post('/theme/')
def create_or_update_theme(theme: schema_church.ThemeCreate, uow: UnitOfWork = Depends(get_db)) -> Optional[schema_church.Theme]:
    return church_service.ChurchThemeService(uow).create_or_update_theme(theme) 

@router.get('/theme/{church_id}/{year}')
def get_theme_by_church_id_and_year(church_id: str, year: int, uow: UnitOfWork = Depends(get_db)):
    return church_service.ChurchThemeService(uow).get_theme_by_church_id_and_year(church_id, year)