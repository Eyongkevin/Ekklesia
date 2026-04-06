from sqladmin import Admin
from app.db.session import engine

from app.admin.auth import AdminAuth
from app.admin.views import UserAdmin, ChurchAdmin, MembershipAdmin
from app.core.config import settings


def setup_admin(app):
    admin = Admin(
        app,
        engine,
        authentication_backend=AdminAuth(secret_key=settings.SECRET_KEY),
    )

    # Register views
    admin.add_view(UserAdmin)
    admin.add_view(ChurchAdmin)
    admin.add_view(MembershipAdmin)