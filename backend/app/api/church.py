from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.church import ChurchService
from app.core.schemas.church import Church, ChurchCreate

router = APIRouter(prefix="/churches", tags=["churches"])

@router.post("/")
def create(church: ChurchCreate, db: Session = Depends(get_db)) -> Church:
    return ChurchService.create_church(db, church.name)

@router.get("/")
def list_churches(db: Session = Depends(get_db)) -> list[Church]:
    return ChurchService.get_churches(db)