import marshmallow.fields as ma
from marshmallow import pre_dump
from loguru import logger

from momenttrack_shared_models.core.extensions import db
from momenttrack_shared_models.core.schemas._base import BaseMASchema, BaseSQLAlchemyAutoSchema
from marshmallow import fields
from momenttrack_shared_models.core.database.models import (
    LicensePlate,
    LicensePlateMove,
    Location,
    ProductionOrder,
    Product,
    BinFamily,
    Pick, PickTypeEnum
)
from momenttrack_shared_models.core.database.models import Bin
from momenttrack_shared_models.core.schemas.location_schema import LocationSchema
from momenttrack_shared_models.core.schemas.vendor_schema import VendorSchema
from momenttrack_shared_models.core.database.models import ShoppingList
from momenttrack_shared_models.core.schemas.production_order_lineitem_schema import (
    ProductionOrderLineitemSchema,
)


class InvalidLengthError(Exception):
    pass


class PRIDField(fields.Field):
    #: Default error messages.
    default_error_messages = {
        "invalid": "Not a valid 'LpMoveField' value.",
        "length": "Invalid length for field value",
    }

    def __init__(self, allowed_len=None, **kwargs):
        super().__init__(**kwargs)
        self.allowed_len = allowed_len

    def _verifyData(self, val):
        int_cond = isinstance(val, int)
        str_cond = isinstance(val, str)

        assert (int_cond or str_cond) is True

        if str_cond:
            try:
                val = ProductionOrder.query.filter_by(docid=val).first().id
            except Exception:
                val = None

        return val

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        try:
            return self._verifyData(value)
        except AssertionError as e:
            logger.error(e)
            raise self.make_error("invalid")

        except InvalidLengthError as e:
            logger.error(e)
            raise self.make_error("length")

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        try:
            return self._verifyData(value)
        except AssertionError as e:
            logger.error(e)
            raise self.make_error("invalid")

        except InvalidLengthError as e:
            logger.error(e)
            raise self.make_error("length")


class LpMoveField(fields.Field):
    #: Default error messages.
    default_error_messages = {
        "invalid": "Not a valid 'LpMoveField' value.",
        "length": "Invalid length for field value",
    }

    def __init__(self, allowed_len=None, **kwargs):
        super().__init__(**kwargs)
        self.allowed_len = allowed_len

    def _verifyData(self, val):
        int_cond = isinstance(val, int)
        str_cond = isinstance(val, str)

        assert (int_cond or str_cond) is True

        if str_cond:
            try:
                assert len(val) is self.allowed_len
            except AssertionError:
                raise InvalidLengthError

        return val

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        try:
            return self._verifyData(value)
        except AssertionError as e:
            raise self.make_error("invalid")
            logger.error(e)
        except InvalidLengthError as e:
            raise self.make_error("length")
            logger.error(e)

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        try:
            return self._verifyData(value)
        except AssertionError as e:
            raise self.make_error("invalid")
            logger.error(e)
        except InvalidLengthError as e:
            raise self.make_error("length")
            logger.error(e)


class LicensePlateList(fields.List):
    def _validate(self, value):
        for item in value:
            if not (
                isinstance(item, str) and len(item) == 25
            ) and not isinstance(
                item, int
            ):
                raise ValueError(
                    "List elements must be strings with "
                    "a length of 25 or integers"
                )


class LicensePlateSwaggerSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True, required=False)  # read-only
    location_id = ma.Integer(required=False)  # optional field
    # product = fields.Nested(ProductSchema, only=("part_number",))

    class Meta:
        exclude = ("updated_at",)
        model = LicensePlate
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True


class SwaggerMadeManyRequestSchema(LicensePlateSwaggerSchema):
    # lp_ids = ma.String(required=True, many=True)

    lp_ids = ma.List(ma.String(required=True))

    production_order_id = PRIDField(required=True)

    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True, required=False)  # read-only

    class Meta:
        exclude = (
            "updated_at", "id",
            "created_at", "organization_id",
            "redirect_url", "external_serial_number",
            "parent_license_plate_id", "is_consumer_facing",
            "lp_id"
        )
        model = LicensePlate
        sqla_session = db.session
        load_instance = False
        # include_relationships = True
        # include_fk = True


class SwaggerPlateMadeItRequestSchema(LicensePlateSwaggerSchema):
    # lp_ids = ma.String(required=True, many=True)
    id = ma.Int(dump_only=True)
    production_order_id = PRIDField(required=True)

    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True, required=False)  # read-only

    class Meta:
        exclude = (
            "updated_at", "id",
            "created_at", "organization_id",
            "redirect_url", "external_serial_number",
            "parent_license_plate_id", "is_consumer_facing"
        )
        model = LicensePlate
        sqla_session = db.session
        load_instance = False
        # include_relationships = True
        # include_fk = True


class SwaggerProductSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True)  # read-only
    # preferred_vendor = ma.Nested("VendorSchema", dump_only=True)  # read-only

    class Meta:
        exclude = ("updated_at",)
        model = Product
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True


class LicensePlateMoveLogsSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True, data_key="arrived_at")  # read-only
    left_at = ma.String()

    class Meta:
        exclude = (
            "updated_at",
            "organization_id",
            "trx_id",
        )
        model = LicensePlateMove
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True

    @pre_dump
    def normalize_date(self, obj, *args, **kwargs):
        if obj:
            obj.created_at = obj.created_at.strftime("%Y-%m-%d %H:%M:%S.%f")
            if obj.left_at:
                obj.left_at = obj.left_at.strftime("%Y-%m-%d %H:%M:%S.%f")
        return obj


class SwaggerLocationReportSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True, required=False)  # read-only
    oldest_license_plate = ma.Nested(
        LicensePlateSwaggerSchema(
            only=("id", "lp_id", "product_id", "quantity", "product")
        )
    )
    # current_user = ma.Nested("UserSchema")
    license_plates = ma.Nested(
        LicensePlateSwaggerSchema(
            only=(
                "id",
                "lp_id",
                "product_id",
                "quantity",
                "product",
                "external_serial_number",
            )
        ),
        many=True,
    )
    logs = ma.Nested(LicensePlateMoveLogsSchema, many=True)
    average_duration = ma.String()  # external
    oldest_log = ma.Nested(LicensePlateMoveLogsSchema)
    latest_log = ma.Nested(LicensePlateMoveLogsSchema)

    class Meta:
        exclude = ("updated_at",)
        model = Location
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True


class SwaggerBinSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True, required=False)  # read-only
    # bin_family = ma.Nested(BinFamilySchema, dump_only=True)

    class Meta:
        exclude = ("updated_at",)
        model = Bin
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True


class SwaggerBinFamilySchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True, required=False)  # read-only

    product = ma.Nested(SwaggerProductSchema, dump_only=True)
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


class SwaggerShoppingListSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    activity_id = ma.Integer(dump_only=True)  # read-only
    created_at = ma.String(dump_only=True)  # read-only
    user_id = ma.Integer(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True, required=False)  # read-only

    bin = ma.Nested(SwaggerBinSchema, dump_only=True)
    location = ma.Nested(LocationSchema, dump_only=True)
    product = ma.Nested(SwaggerProductSchema, dump_only=True)
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


class SwaggerProductionOrderSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    # created_at = ma.String(dump_only=True)  # read-only

    organization_id = ma.Integer(dump_only=True)  # read-only
    user_id = ma.Integer(dump_only=True)  # read-only

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


class SwaggerProductionOrderPaginatedListSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    docid = ma.String(dump_only=True)  # read-only
    external_docid = ma.String(dump_only=True)  # read-only
    product_id = ma.Integer(dump_only=True)  # read-only

    requested_qty = ma.Integer(dump_only=True)  # read-only
    location_id = ma.Integer(dump_only=True)  # read-only
    actual_start_date = ma.String(dump_only=True)  # read-only
    actual_end_date = ma.String(dump_only=True)  # read-only
    planned_start_date = ma.String(dump_only=True)  # read-only
    planned_end_date = ma.String(dump_only=True)  # read-only
    redirect_url = ma.String(dump_only=True)  # read-only
    status = ma.String(dump_only=True)  # read-only
    user_id = ma.Integer(dump_only=True)  # read-only

    organization_id = ma.Integer(dump_only=True)  # read-only
    created_at = ma.String(dump_only=True)  # read-only

    class Meta:
        model = ProductionOrder
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True


class SwaggerProductionOrderStatusReportSchema(BaseMASchema):
    """output schema for ProductionOrderStatusReportSchema"""

    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True)  # read-only
    docid = ma.String(dump_only=True)  # read-only


class SwaggerProductionOrderPublicViewPermUpdate(BaseMASchema):
    """validation schema for permissions from client"""

    def verify_weight(val):
        current_perms = [2, 4, 8, 16, 32, 64, 128]
        return not val % 2 and val in current_perms

    add = ma.List(fields.Integer(validate=verify_weight))
    remove = ma.List(fields.Integer(validate=verify_weight))


class SwaggerProductionOrderSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only

    organization_id = ma.Integer(dump_only=True)  # read-only
    user_id = ma.Integer(dump_only=True)  # read-only
    # user = ma.Nested(
    #     "UserSchema", dump_only=True, only=("first_name", "id", "person_id", "status")
    # )  # read-only

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
