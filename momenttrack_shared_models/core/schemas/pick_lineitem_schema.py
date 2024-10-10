import marshmallow.fields as ma

from momenttrack_shared_models.core.schemas._base import BaseSQLAlchemyAutoSchema
from momenttrack_shared_models.core.database.models import PickLineitem
from momenttrack_shared_models.core.extensions import db


class PickLineitemSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True)  # read-only

    class Meta:
        exclude = ("updated_at",)
        model = PickLineitem
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True
