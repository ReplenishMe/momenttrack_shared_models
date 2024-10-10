import marshmallow.fields as ma

from momenttrack_shared_models.core.schemas._base import BaseMASchema, BaseSQLAlchemyAutoSchema
from momenttrack_shared_models.core.schemas.location_schema import LocationSchema
from momenttrack_shared_models.core.schemas.product_schema import ProductSchema
from momenttrack_shared_models.core.schemas.vendor_schema import VendorSchema
from momenttrack_shared_models.core.database.models import BinFamily
from momenttrack_shared_models.core.extensions import db


class BinFamilySchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True, required=False)  # read-only

    product = ma.Nested(ProductSchema, dump_only=True)
    location = ma.Nested(LocationSchema, dump_only=True)
    preferred_vendor = ma.Nested(VendorSchema, dump_only=True)

    class Meta:
        exclude = ("updated_at",)
        model = BinFamily
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True


class BinFamilyRelocateSchema(BaseMASchema):
    location_id = ma.Integer(required=True)
