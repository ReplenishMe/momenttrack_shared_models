import marshmallow.fields as ma

from momenttrack_shared_models.core.schemas._base import BaseMASchema, BaseSQLAlchemyAutoSchema
from momenttrack_shared_models.core.schemas.location_schema import LocationSchema
from momenttrack_shared_models.core.schemas.production_order_lineitem_schema import (
    ProductionOrderLineitemSchema,
)
from momenttrack_shared_models.core.database.models import ProductionOrder
from momenttrack_shared_models.core.extensions import db
from marshmallow import fields


class ProductionOrderSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    # created_at = ma.String(dump_only=True)  # read-only

    organization_id = ma.Integer(dump_only=True)  # read-only
    user_id = ma.Integer(dump_only=True)  # read-only
    user = ma.Nested(
        "UserSchema",
        dump_only=True,
        only=("first_name", "id", "person_id", "status")
    )  # read-only
    product = ma.Nested("ProductSchema", dump_only=True)

    production_order_lineitems = ma.Nested(
        ProductionOrderLineitemSchema(
            only=(
                "id",
                "created_at",
                "license_plate_id",
                "license_plate_move_id",
                "qty",
                "status",
            )
        ),
        many=True,
        data_key="lineitems",
    )

    class Meta:
        exclude = ("updated_at",)
        model = ProductionOrder
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True


class ProductionOrderListSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    # created_at = ma.String(dump_only=True)  # read-only

    organization_id = ma.Integer(dump_only=True)  # read-only
    user_id = ma.Integer(dump_only=True)  # read-only
    user = ma.Nested(
        "UserSchema",
        dump_only=True,
        only=("first_name", "id", "person_id", "status")
    )  # read-only
    product = ma.Nested("ProductSchema", dump_only=True)

    class Meta:
        exclude = ("updated_at",)
        model = ProductionOrder
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True


class ProductionOrderPaginatedListSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    docid = ma.String(dump_only=True)  # read-only
    external_docid = ma.String(dump_only=True)  # read-only
    product_id = ma.Integer(dump_only=True)  # read-only
    product = ma.Nested(
        "ProductSchema",
        dump_only=True,
        only=("id", "part_number", "description", "uom"),
    )
    requested_qty = ma.Integer(dump_only=True)  # read-only
    location_id = ma.Integer(dump_only=True)  # read-only
    actual_start_date = ma.String(dump_only=True)  # read-only
    actual_end_date = ma.String(dump_only=True)  # read-only
    planned_start_date = ma.String(dump_only=True)  # read-only
    planned_end_date = ma.String(dump_only=True)  # read-only
    redirect_url = ma.String(dump_only=True)  # read-only
    status = ma.String(dump_only=True)  # read-only
    user_id = ma.Integer(dump_only=True)  # read-only
    user = ma.Nested(
        "UserSchema",
        dump_only=True, only=("first_name", "id", "person_id", "status")
    )

    organization_id = ma.Integer(dump_only=True)  # read-only
    created_at = ma.String(dump_only=True)  # read-only

    class Meta:
        model = ProductionOrder
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True


class ProductionOrderStatusReportLineitemSchema(BaseMASchema):
    """output schema for ProductionOrderStatusReportLineitemSchema"""

    id = ma.Int(dump_only=True)
    license_plate_id = ma.Int(dump_only=True)  # read-only
    lp_id = ma.String(dump_only=True)  # read-only
    # product_id = ma.Int(dump_only=True)  # read-only
    # product = ma.Nested(
    #     ProductSchema(
    #       only=("description", "part_number", "uom", "id")),
    #       dump_only=True
    # )
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
    product = ma.Nested("ProductSchema", dump_only=True)
    lineitems = ma.Nested(ProductionOrderStatusReportLineitemSchema, many=True)
    order_template = ma.Dict(dump_only=True)
    # lineitems = ma.Nested(ProductionOrderLineitemSchema, many=True)


class ProductionOrderPublicViewPermUpdate(BaseMASchema):
    """validation schema for permissions from client"""

    def verify_weight(val):
        current_perms = [2, 4, 8, 16, 32, 64, 128]
        return not val % 2 and val in current_perms

    add = ma.List(fields.Integer(validate=verify_weight))
    remove = ma.List(fields.Integer(validate=verify_weight))
