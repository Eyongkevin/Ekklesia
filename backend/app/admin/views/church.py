from sqladmin import ModelView

from app.models import Church


class ChurchAdmin(ModelView, model=Church):
    column_list = [Church.id, Church.name, Church.code, Church.is_active]
    column_searchable_list = [Church.name, Church.code]
    # column_filters = [Church.is_active]