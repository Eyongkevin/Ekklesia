from fastapi import APIRouter, Depends

from app.api.deps import get_db
from app.services import permission as permission_services
from app.schemas import permission as permission_schemas
from app.db.uow import UnitOfWork


router = APIRouter(prefix="/permission", tags=["permission"])



@router.get("/", response_model=list[permission_schemas.PermissionRes])
def permissions(uow: UnitOfWork = Depends(get_db)):
    return permission_services.PermissionService(uow).get_permissions()
