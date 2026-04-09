import random

from sqladmin import ModelView
from sqladmin.filters import BooleanFilter
from wtforms.validators import DataRequired
from wtforms import StringField

from app.models import Church

IGNORE = {"of", "the", "and"}
class ChurchAdmin(ModelView, model=Church):
    create_template = "sqladmin/custom_create.html"
    column_list = [Church.name, Church.code, Church.is_active]
    column_searchable_list = [Church.name, Church.code]
    column_filters = [
        BooleanFilter(Church.is_active, parameter_name="Active"),
    ]

    form_columns = [
        "name",
        "is_active"
    ]

    form_args = {
        "name": {
            "label": "Name",
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

    async def scaffold_form(self, *args, **kwargs):
        """Override scaffold_form to inject code field."""

        form_class = await super().scaffold_form()

        form_class.code = StringField(
            "Code",
            render_kw={
                "class": "form-control",
                "placeholder": "Code auto-generated from name",
                "readonly": True
            },
            validators=[DataRequired()]
        )

        return form_class
    
    async def on_model_change(self, form: dict[str, str | bool], model, is_created, *args, **kwargs) -> None:
        """Override on_model_change to generate church code if not handled in UI."""

        if not form.get('code'):
            model.code = generate_code_from_name(form.get('name'))


def generate_code_from_name(name: str, random_length: int = 3) -> str:
    """Generate code for church base on its name

    Get first letters from church name and add random digits

    EG: Faith Baptist Church -> FBC239
    """

    initials = "".join(
        word[0].upper()
        for word in name.strip().split()
        if word.lower() not in IGNORE
    )

    random_part = "".join(
        str(random.randint(0, 9))
        for _ in range(random_length)
    )

    return initials + random_part
