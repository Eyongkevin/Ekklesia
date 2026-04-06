from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.services.user import UserService
from app.services.membership import MembershipService
from app.core.schemas import user as user_schemas
from app.db.uow import UnitOfWork

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = form.get("username")
        password = form.get("password")

        if not email or not password:
            return False

        with UnitOfWork() as uow:
            user_service = UserService(uow)
            member_ship_service = MembershipService(uow)
            user = user_service.authenticate_user(email, password)
            if user and member_ship_service.check_is_super_admin(str(user.id)):
                request.session["user_id"] = str(user.id)
                return True
        return False
    
    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True
    
    async def authenticate(self, request: Request) -> user_schemas.User | RedirectResponse:
        user_id = request.session.get("user_id")
        if user_id:
            with UnitOfWork() as uow:
                user_service = UserService(uow)
                user = user_service.user_crud.get_user_by_id(user_id)
                if user is not None:
                    return user
        return RedirectResponse(url="/admin/login")
            
