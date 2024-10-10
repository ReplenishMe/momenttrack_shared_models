import marshmallow.fields as ma

from momenttrack_shared_models.core.schemas._base import BaseSQLAlchemyAutoSchema
from momenttrack_shared_models.core.database.models import Role
from momenttrack_shared_models.core.extensions import db


class RoleSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only

    class Meta:
        exclude = ("updated_at", "permissions", "organization_id", "role_type")
        model = Role
        sqla_session = db.session
        load_instance = True
        # include_relationships = True
        include_fk = True
