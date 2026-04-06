from sqladmin import ModelView
from app.models import User
from app.models import Church
from app.models import Membership


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.first_name, User.email, User.is_active]
    column_searchable_list = [User.email]
    column_sortable_list = [User.created_at, User.modified_at]
    # column_filters = [User.is_active]


class ChurchAdmin(ModelView, model=Church):
    column_list = [Church.id, Church.name, Church.code, Church.is_active]
    column_searchable_list = [Church.name, Church.code]
    # column_filters = [Church.is_active]


class MembershipAdmin(ModelView, model=Membership):
    column_list = [
        Membership.id,
        Membership.user_id,
        Membership.church_id,
        Membership.role,
        Membership.is_active,
    ]
    # column_filters = [Membership.role, Membership.is_active]
