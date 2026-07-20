from sqladmin import Admin
from app.db.session import engine

from app.admin.auth import AdminAuth
from app.admin import views
from app.core.config import settings


def setup_admin(app):
    admin = Admin(
        app,
        engine,
        authentication_backend=AdminAuth(secret_key=settings.SECRET_KEY),
        templates_dir="app/admin/templates"
    )

    # Register views
    admin.add_view(views.UserAdmin)
    admin.add_view(views.ChurchAdmin)
    admin.add_view(views.SystemRoleAdmin)
    admin.add_view(views.MembershipAdmin)
    admin.add_view(views.AnnouncementStatusAdmin)
    admin.add_view(views.AnnouncementTagAdmin)
    admin.add_view(views.AnnouncementAudienceAdmin)
