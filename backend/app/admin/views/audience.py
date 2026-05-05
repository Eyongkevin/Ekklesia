from sqladmin import ModelView
from sqladmin.filters import BooleanFilter
from wtforms.validators import DataRequired, Optional

from app.models import AnnouncementAudience
from app.core.utils import format_datetime
from app.admin.utils import get_short_desc


class AnnouncementAudienceAdmin(ModelView, model=AnnouncementAudience):
    column_list = [AnnouncementAudience.name, 'description', AnnouncementAudience.is_active, AnnouncementAudience.created_at]
    column_searchable_list = [AnnouncementAudience.name]
    column_sortable_list = [AnnouncementAudience.created_at, AnnouncementAudience.modified_at]
    column_filters = [
        BooleanFilter(AnnouncementAudience.is_active, parameter_name="Active"),
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