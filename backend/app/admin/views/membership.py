from operator import or_
from sqladmin import ModelView
from sqlalchemy.orm import joinedload
from sqladmin.filters import BooleanFilter
from wtforms.validators import DataRequired, Optional
from wtforms import SelectField

from app.models import Membership
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
    column_list = [
        "First Name",
        "Email",
        "Church Name",
        "Role",
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
        "Role": lambda m, a: m.role.replace("_", " ").title() if m.role else "N/A",
    }

    form_overrides = {
        'role': SelectField
    }

    form_columns = [
        "user",
        "church",
        "role",
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
        "role": {
            "label": "Role",
            "choices": ROLE_CHOICES,
            "validators": [DataRequired()]
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

        # Eager load church relationship to avoid N+1 problem when displaying church names
        query = query.filter(
            or_(
                Membership.role == "super_admin",
                Membership.role == "church_admin"
            )
        )

        return query

