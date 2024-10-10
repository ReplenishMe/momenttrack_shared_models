import marshmallow.fields as ma

from momenttrack_shared_models.core.schemas._base import BaseSQLAlchemyAutoSchema
from momenttrack_shared_models.core.schemas.bin_schema import BinSchema
from momenttrack_shared_models.core.schemas.location_schema import LocationSchema
from momenttrack_shared_models.core.schemas.product_schema import ProductSchema
from momenttrack_shared_models.core.schemas.vendor_schema import VendorSchema
from momenttrack_shared_models.core.database.models import ShoppingList
from momenttrack_shared_models.core.extensions import db


class ShoppingListSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    activity_id = ma.Integer(dump_only=True)  # read-only
    created_at = ma.String(dump_only=True)  # read-only
    user_id = ma.Integer(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True, required=False)  # read-only

    bin = ma.Nested(BinSchema, dump_only=True)
    location = ma.Nested(LocationSchema, dump_only=True)
    product = ma.Nested(ProductSchema, dump_only=True)
    vendor = ma.Nested(VendorSchema, dump_only=True)

    class Meta:
        exclude = ("updated_at",)
        model = ShoppingList
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True


class ShoppingListExportSchema(BaseSQLAlchemyAutoSchema):
    created_at = ma.String(dump_only=True)  # read-only
    user_id = ma.Integer(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True, required=False)  # read-only

    user = ma.Function(lambda obj: obj.user.first_name, dump_only=True)
    product = ma.Function(lambda obj: obj.product.name, dump_only=True)

    class Meta:
        exclude = ("updated_at",)
        model = ShoppingList
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True
