import marshmallow.fields as ma

from momenttrack_shared_models.core.schemas import ProductSchema
from momenttrack_shared_models.core.schemas._base import BaseMASchema, BaseSQLAlchemyAutoSchema
from momenttrack_shared_models.core.schemas.location_schema import LocationSchema
from momenttrack_shared_models.core.database.models import Pick, PickLineitem, PickTypeEnum
from momenttrack_shared_models.core.extensions import db


class ProductionOrderLineitemSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True)  # read-only
    pick_id = ma.Integer(data_key="production_order_id")
    product = ma.Nested(
        ProductSchema(
            only=("description", "part_number", "id")
        ),
        dump_only=True
    )

    class Meta:
        exclude = ("updated_at", "pick")
        model = PickLineitem
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True


class ProductionOrderSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only

    organization_id = ma.Integer(dump_only=True)  # read-only
    user_id = ma.Integer(dump_only=True)  # read-only
    user = ma.Nested(
        "UserSchema", dump_only=True,
        only=("first_name", "id", "person_id", "status")
    )  # read-only

    pick_type = ma.Constant(PickTypeEnum.PRODUCTIONORDER, load_only=True)
    pick_lineitems = ma.Nested(
        ProductionOrderLineitemSchema,
        many=True,
        data_key="lineitems",
    )

    class Meta:
        exclude = ("updated_at",)
        model = Pick
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True


class ProductionOrderStatusReportLineitemSchema(BaseMASchema):
    """output schema for ProductionOrderStatusReportLineitemSchema"""

    id = ma.Int(dump_only=True)
    license_plate_id = ma.Int(dump_only=True)  # read-only
    lp_id = ma.String(dump_only=True)  # read-only
    product_id = ma.Int(dump_only=True)  # read-only
    product = ma.Nested(
        ProductSchema(
            only=("description", "part_number", "uom", "id")
        ),
        dump_only=True
    )
    location_id = ma.Int(dump_only=True)  # read-only
    location = ma.Nested(
        LocationSchema(only=("beacon_id", "location_type", "name", "active"))
    )  # read-only
    status = ma.String(dump_only=True)  # read-only
    external_serial_number = ma.String(dump_only=True)  # read-only


class ProductionOrderStatusReportSchema(BaseMASchema):
    """output schema for ProductionOrderStatusReportSchema"""

    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True)  # read-only
    docid = ma.String(dump_only=True)  # read-only
    lineitems = ma.Nested(ProductionOrderStatusReportLineitemSchema, many=True)
