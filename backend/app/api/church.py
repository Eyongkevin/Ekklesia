from typing import Optional

from fastapi import APIRouter, Depends


from app.api.deps import get_db
from app.services import church as church_services
from app.schemas import church as church_schemas
from app.db.uow import UnitOfWork


router = APIRouter(prefix="/churches", tags=["churches, contact, announcement"])



@router.post("/", response_model=church_schemas.Church)
def create(church: church_schemas.ChurchCreate, uow: UnitOfWork = Depends(get_db)):
    return church_services.ChurchService(uow).create_church(church.name)


@router.get("/", response_model=list[church_schemas.Church])
def list_churches(uow: UnitOfWork = Depends(get_db)):
    return church_services.ChurchService(uow).get_churches()


@router.get('/{church_id}', response_model=Optional[church_schemas.Church])
def get_church(church_id: str, uow: UnitOfWork = Depends(get_db)):
    return church_services.ChurchService(uow).get_church_by_id(church_id)


@router.get('/user/{user_id}', response_model=Optional[church_schemas.Church])
def get_user_church(user_id: str, uow: UnitOfWork = Depends(get_db)):
    return church_services.ChurchService(uow).get_church_by_user_id(user_id)


# CONTACT
@router.post('/contact/', response_model=Optional[church_schemas.Contact])
def create_or_update_contact(contact: church_schemas.ContactCreate, uow: UnitOfWork = Depends(get_db)):
    return church_services.ChurchContactService(uow).create_or_update_contact(contact)


@router.get('/contact/{church_id}', response_model=Optional[church_schemas.Contact])
def get_church_contact(church_id: str, uow: UnitOfWork = Depends(get_db)):
    return church_services.ChurchContactService(uow).get_church_contact_by_church_id(church_id)


# THEME
@router.post('/theme/', response_model=Optional[church_schemas.Theme])
def create_or_update_theme(theme: church_schemas.ThemeCreate, uow: UnitOfWork = Depends(get_db)):
    return church_services.ChurchThemeService(uow).create_or_update_theme(theme)


@router.get('/theme/{church_id}/{year}', response_model=Optional[church_schemas.Theme])
def get_theme_by_church_id_and_year(church_id: str, year: int, uow: UnitOfWork = Depends(get_db)):
    return church_services.ChurchThemeService(uow).get_theme_by_church_id_and_year(church_id, year)
