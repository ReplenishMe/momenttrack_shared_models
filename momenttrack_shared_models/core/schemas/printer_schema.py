import marshmallow.fields as ma

from momenttrack_shared_models.core.schemas._base import \
    BaseSQLAlchemyAutoSchema
from momenttrack_shared_models.core.schemas.utils import current_org
from momenttrack_shared_models.core.database.models import Printer
from momenttrack_shared_models.core.extensions import db
from marshmallow import ValidationError, validates_schema


class PrinterSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True)  # read-only

    class Meta:
        exclude = ("updated_at",)
        model = Printer
        sqla_session = db.session
        load_instance = True
        include_fk = True

    @validates_schema
    def validator(self, data, **kwargs):
        errors = {}
        if Printer.get_by_name_and_org(data["name"], current_org):
            errors["name"] = ["printer name already exists"]

        if errors:
            raise ValidationError(errors)
