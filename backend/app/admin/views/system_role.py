from sqladmin import ModelView
from sqladmin.filters import BooleanFilter
from wtforms.validators import DataRequired, Optional

from app.models import SystemRole
from app.core.utils import format_datetime
from app.admin.utils import get_short_desc


class SystemRoleAdmin(ModelView, model=SystemRole):
    column_list = [SystemRole.name, 'description', SystemRole.is_active, SystemRole.version, SystemRole.created_at]
    column_searchable_list = [SystemRole.name, SystemRole.version]
    column_sortable_list = [SystemRole.created_at, SystemRole.modified_at]
    column_filters = [
        BooleanFilter(SystemRole.is_active, parameter_name="Active"),
    ]

    column_formatters = {
        "description": lambda m, a: get_short_desc(m.description),
        "created_at": lambda m, a: format_datetime(m.created_at)
    }

    form_columns = [
        "name",
        "version",
        "is_active",
        "permissions",
        "description",
    ]

    form_args = {
        "name": {
            "label": "Name",
            "validators": [DataRequired()],
        },
        "version": {
            "label": "Version",
            "validators": [DataRequired()],
        },
        "permissions": {
            "label": "Permissions",
            "validators": [DataRequired()],
        },
        "description": {
            "label": "Description",
            "validators": [Optional()]
        },
    }
    form_widget_args = {
        "is_active": {
            "checked": True
        },
        "version": {
            "value": 1
        },
    }