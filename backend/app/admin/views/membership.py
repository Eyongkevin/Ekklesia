from fastapi import Request
from operator import or_
from sqladmin import ModelView, expose
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqladmin.filters import BooleanFilter
from wtforms.validators import DataRequired, Optional
from wtforms import SelectField
from starlette.responses import RedirectResponse

from app.models import Membership, Role
from app.models import User
from app.services.user import UserService
from app.db.uow import UnitOfWork
from app.core.utils import format_datetime
from app.core.utils import MembershipRole


ROLE_CHOICES = [
    (r.value, ' '.join(r.value.split('_')).title()) for r in MembershipRole
]

def get_first_name(user_id: str) -> str:
    with UnitOfWork() as uow:
        user_service = UserService(uow)
        user = user_service.get_user_by_id(user_id)
        return user.first_name if user and user.first_name else "N/A"
    
def get_email(user_id: str) -> str:
    with UnitOfWork() as uow:
        user_service = UserService(uow)
        user = user_service.get_user_by_id(user_id)
        return user.email if user and user.email else "N/A"


class MembershipAdmin(ModelView, model=Membership):
    list_template = "sqladmin/custom_list.html"
    column_list = [
        "First Name",
        "Email",
        "Church Name",
        Membership.is_active,
        "Created At",
    ]
    # TODO: Search by first_name, church_name
    # column_searchable_list = [User.first_name]
    column_filters = [
        BooleanFilter(Membership.is_active, parameter_name="Active"),
        # TODO: Filter by role
    ]
    
    column_formatters = {
        "First Name": lambda m, a: get_first_name(m.user_id),
        "Email": lambda m, a: get_email(m.user_id),
        "Church Name": lambda m, a: m.church.name if m.church else "N/A",
        "Created At": lambda m, a: format_datetime(m.created_at),
        # "Role": lambda m, a: m.role.replace("_", " ").title() if m.role else "N/A",
    }

    form_columns = [
        "user",
        "church",
        "is_active"
    ]

    form_args = {
        "user": {
            "label": "User",
            "validators": [DataRequired()],
        },
        "church": {
            "label": "Church",
            "validators": [Optional()]
        },
        "is_active": {
            "label": "Is Active",
            "validators": [DataRequired()]
        }
    }
    form_widget_args = {
        "is_active": {
            "checked": True
        },
    }

    def list_query(self, request):
        """Override list_query to filter users based on their memberships and roles."""

        query = super().list_query(request)

        # query = query.join(Membership.church)
        query = query.join(Membership.user)

        query = query.options(
            joinedload(Membership.church)
        )

        query = query.options(
            joinedload(Membership.roles)
        )

        # Eager load church relationship to avoid N+1 problem when displaying church names
        # query = query.filter(
        #     or_(
        #         Membership.role == "super_admin",
        #         # Membership.role == "church_admin"
        #         Membership.roles.any(
        #             Role.name.in_(["Super Admin", "Church Admin"])
        #         )
        #     )
        # )

        return query

    def roles_url(self, request: Request, obj: Membership) -> str:
        return f"/admin/membership/roles/{obj.id}"
    
    @expose("/roles/{pk}", methods=["GET", "POST"])
    async def manage_roles(self, request: Request):
        pk = request.path_params["pk"]

        with UnitOfWork() as uow:
            membership = (
                uow.db.execute(
                    select(Membership)
                    .options(
                        joinedload(Membership.roles),
                        joinedload(Membership.user),
                        joinedload(Membership.church),
                    )
                    .where(Membership.id == pk)
                )
                .unique()
                .scalar_one()
            )

            roles = (
                uow.db.execute(
                    select(Role)
                    .where(Role.church_id == membership.church_id)
                    .order_by(Role.name)
                )
                .scalars()
                .all()
            )

            if request.method == "POST":
                form = await request.form()

                selected_role_ids = form.getlist("roles")

                selected_roles = (
                    uow.db.execute(
                        select(Role).where(Role.id.in_(selected_role_ids))
                    )
                    .scalars()
                    .all()
                )

                membership.roles = selected_roles

                uow.commit()

                return RedirectResponse(
                    url="/admin/membership/list",
                    status_code=303,
                )

        return await self.templates.TemplateResponse(
            request=request,
            name="sqladmin/manage_roles.html",
            context={
                "membership": membership,
                "roles": roles,
            },
        )
