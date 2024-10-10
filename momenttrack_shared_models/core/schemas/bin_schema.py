import marshmallow.fields as ma

from momenttrack_shared_models.core.schemas._base import \
     BaseSQLAlchemyAutoSchema
from momenttrack_shared_models.core.schemas.bin_family_schema import \
     BinFamilySchema
from momenttrack_shared_models.core.database.models import Bin
from momenttrack_shared_models.core.extensions import db


class BinSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True, required=False)  # read-only
    bin_family = ma.Nested(BinFamilySchema, dump_only=True)

    class Meta:
        exclude = ("updated_at",)
        model = Bin
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True
