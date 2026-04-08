from sqladmin import ModelView

from app.models import Membership


class MembershipAdmin(ModelView, model=Membership):
    column_list = [
        Membership.id,
        Membership.user_id,
        Membership.church_id,
        Membership.role,
        Membership.is_active,
    ]
    # column_filters = [Membership.role, Membership.is_active]
