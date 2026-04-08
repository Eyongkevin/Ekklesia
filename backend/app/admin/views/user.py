from operator import or_

from sqladmin import ModelView
from sqlalchemy.orm import joinedload
from sqladmin.filters import BooleanFilter
from wtforms import PasswordField
from wtforms.validators import DataRequired

from app.models import User
from app.models import Membership
from app.core.utils import hash_password

def get_church(user) -> str:
    if user.memberships:
        membership = user.memberships[0]
        if membership.church:
            return membership.church.name
    return "N/A"

def get_role(user):
    if user.memberships:
        membership = user.memberships[0]
        return membership.role
    return "N/A"


class UserAdmin(ModelView, model=User):
    column_list = [User.first_name, User.email, "church", "role", User.is_active]
    column_searchable_list = [User.email]
    column_sortable_list = [User.created_at, User.modified_at]
    column_filters = [
        BooleanFilter(User.is_active, parameter_name="Active"),
        # TODO: Filter by role
    ]

    column_formatters = {
        "church": lambda m, a: get_church(m),
        "role": lambda m, a: get_role(m)
    }

    # Customize Form

    form_columns = [
        "first_name",
        "email",
        "is_active",
    ]

    form_args = {
        "email": {
            "label": "Email Address",
            "validators": [DataRequired()],
        },
        "first_name": {
            "label": "First Name",
            "validators": [DataRequired()],
        },
    }
    form_widget_args = {
        "is_active": {
            "checked": True
        },
        "password": {
            "placeholder": "Enter password",
        },
        "first_name": {
            "placeholder": "Enter first name",
        },
        "email": {
            "placeholder": "Enter email address",
        }
    }

    async def scaffold_form(self, *args, **kwargs):
        """Override scaffold_form to inject password field."""

        form_class = await super().scaffold_form()

        form_class.password = PasswordField(
            "Password", validators=[DataRequired()]
        )

        return form_class

    async def on_model_change(self, form: dict[str, str | bool], model, is_created, *args, **kwargs) -> None:
        """Override on_model_change to handle password hashing."""

        password: str = form["password"]

        if password:
            model.password_hash = hash_password(password)

    def list_query(self, request):
        """Override list_query to filter users based on their memberships and roles."""

        query = super().list_query(request)

        query = query.join(User.memberships)

        # Eager load church relationship to avoid N+1 problem when displaying church names
        query = query.options(
            joinedload(User.memberships).joinedload(Membership.church)
        )
        query = query.filter(
            or_(
                Membership.role == "super_admin",
                Membership.role == "church_admin"
            )
        )
        
        return query.distinct()
