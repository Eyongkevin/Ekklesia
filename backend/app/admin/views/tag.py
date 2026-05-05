from sqladmin import ModelView
from sqladmin.filters import BooleanFilter
from wtforms.validators import DataRequired, Optional

from app.models import AnnouncementTag
from app.core.utils import format_datetime
from app.admin.utils import get_short_desc


class AnnouncementTagAdmin(ModelView, model=AnnouncementTag):
    column_list = [AnnouncementTag.name, 'description', AnnouncementTag.is_active, AnnouncementTag.created_at]
    column_searchable_list = [AnnouncementTag.name]
    column_sortable_list = [AnnouncementTag.created_at, AnnouncementTag.modified_at]
    column_filters = [
        BooleanFilter(AnnouncementTag.is_active, parameter_name="Active"),
    ]

    column_formatters = {
        "description": lambda m, a: get_short_desc(m.description),
        "created_at": lambda m, a: format_datetime(m.created_at)
    }

    form_columns = [
        "name",
        "description",
        "is_active"
    ]

    form_args = {
        "name": {
            "label": "Name",
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
    }