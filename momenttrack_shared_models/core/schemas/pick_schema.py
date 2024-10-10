import marshmallow.fields as ma

from momenttrack_shared_models.core.schemas._base import BaseSQLAlchemyAutoSchema
from momenttrack_shared_models.core.schemas.pick_lineitem_schema import PickLineitemSchema
from momenttrack_shared_models.core.database.models import Pick
from momenttrack_shared_models.core.extensions import db


class PickSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True)  # read-only
    user_id = ma.Integer(dump_only=True)  # read-only

    pick_lineitems = ma.Nested(PickLineitemSchema, many=True)

    class Meta:
        exclude = ("updated_at",)
        model = Pick
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True
