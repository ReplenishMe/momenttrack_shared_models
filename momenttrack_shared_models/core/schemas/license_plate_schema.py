import marshmallow.fields as ma
from loguru import logger
from marshmallow import (
    fields,
    post_load,
    INCLUDE,
    pre_load
)
from marshmallow.validate import Length, Range
from momenttrack_shared_models.core import messages as MSG
from momenttrack_shared_models.core.schemas._base import (
    BaseMASchema, BaseSQLAlchemyAutoSchema
)
from momenttrack_shared_models.core.database.models import (
    LicensePlate,
    Location,
    ProductionOrder,
    User,
    Product
)
from momenttrack_shared_models.core.extensions import db
from momenttrack_shared_models.core.utils import DataValidationError
from momenttrack_shared_models.core.database.models.license_plate \
     import LicensePlateStatusEnum


class InvalidLengthError(Exception):
    pass


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
                assert len(val) == self.allowed_len
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
            ) and not isinstance(item, int):
                raise ValueError(
                    "List elements must be strings"
                    " with a length of 25 or integers"
                )


class LicensePlateSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True, required=False)  # read-only
    location_id = ma.Integer(required=False)  # optional field
    product = fields.Nested("ProductSchema", only=("part_number",))

    class Meta:
        exclude = ("updated_at",)
        model = LicensePlate
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True

    # @validates_schema
    # def validator(self, data, **kwargs):
    #     errors = {}
    #     if Bin.get_by_name_and_org(data["name"], current_org):
    #         errors["name"] = ["Bin name already exists"]

    #     if errors:
    #         raise ValidationError(errors)


# to resolve circular import error
class ProductDumpSchema2(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True)  # read-only
    preferred_vendor = ma.Nested("VendorSchema", dump_only=True)  # read-only

    class Meta:
        exclude = ("updated_at",)
        model = Product
        sqla_session = db.session
        include_fk = True


# to resolve circular import error
class UserSchemaalt(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    person_id = ma.String(dump_only=True)  # read-only
    created_at = ma.String(dump_only=True)  # read-only

    class Meta:
        exclude = (
            "confirmed_at",
            "updated_at",
            "password",
        )
        model = User
        sqla_session = db.session
        load_instance = True
        # include_relationships = True
        include_fk = True


class LicensePlateMoveOpenSearchSchema(BaseMASchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True, data_key="arrived_at")
    left_at = ma.String()
    status = ma.String()
    license_plate_id = ma.Integer()
    dest_location_id = ma.Integer()
    src_location_id = ma.Integer()

    user_id = ma.Integer()
    product_id = ma.Integer()
    activity_id = ma.Integer()
    product = fields.Method("get_product")
    user = fields.Method("get_user")
    license_plate = fields.Method("get_lp")

    def get_product(self, obj):
        pd = Product.get_by_id(obj.product_id)
        schema = ProductDumpSchema2()
        return schema.dump(pd)

    def get_user(self, obj):
        user = User.get_by_id(obj.user_id)
        schema = UserSchemaalt()
        return schema.dump(user)

    def get_lp(self, obj):
        lp = LicensePlate.get_by_id(obj.license_plate_id)
        schema = {
            "lp_id": lp.lp_id,
            "quantity": lp.quantity,
            "id": lp.id,
            "external_serial_number": lp.external_serial_number,
            "product_id": lp.product_id,
            "product": {
                "part_number": Product.get_by_id(lp.product_id).part_number
            }
        }

        return schema


class LicensePlateOpenSearchSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)
    organization_id = ma.Integer(dump_only=True, required=False)
    location = fields.Nested(
        "LocationSchema", only=(
            "name", "width",
            "height", "beacon_id",
            "depth"
        )
    )
    product = fields.Nested(
        "ProductSchema",
        only=(
            "part_number",
            "description",
        ),
    )

    class Meta:
        model = LicensePlate
        include_relationships = True
        include_fk = True


class LicensePlateSplitSchema(BaseMASchema):
    license_plate_id = ma.Integer(required=True)
    # num_splits = ma.Integer(
    #   required=True, strict=True, validate=Range(min=2)
    # )
    split_distribution = ma.List(
        ma.Float(), required=True, validate=Length(min=1)
    )


class LicensePlateDeductSchema(BaseMASchema):
    license_plate_id = ma.Integer(required=True)
    deduct_qty = ma.Float(
        required=True,
        validate=[
            Range(
                min=0, min_inclusive=False,
                error="deduct_qty must be greater than 0"
            )
        ],
    )


class LicensePlateMoveSchema(BaseMASchema):
    # license_plate_id = ma.Integer(required=True)
    # # num_splits = ma.Integer(
    #   required=True, strict=True, validate=Range(min=2)
    # )
    # dest_location_id = ma.Integer(required=True)
    # user_id = ma.Integer(required=False)
    license_plate_id = LpMoveField(required=True, allowed_len=25)
    dest_location_id = LpMoveField(required=True, allowed_len=11)
    user_id = LpMoveField(required=False, allowed_len=17)

    @post_load
    def add_required_alt(self, data, *args, **kwargs):
        if data:
            if isinstance(data["license_plate_id"], str):
                tmp: [LicensePlate | None] = LicensePlate.query.filter_by(
                    lp_id=data["license_plate_id"]
                ).first()
                if not tmp:
                    raise DataValidationError(
                        MSG.LICENSE_PLATE_NOT_FOUND,
                        MSG.LICENSE_PLATE_NOT_FOUND
                    )
                data["license_plate_id"] = tmp.id
            if isinstance(data["dest_location_id"], str):
                tmp: [Location | None] = Location.query.filter(
                    Location.beacon_id == data["dest_location_id"]
                )
                if not tmp:
                    raise DataValidationError(
                        MSG.LOCATION_NOT_FOUND,
                        MSG.LOCATION_NOT_FOUND
                    )
                data["dest_location_id"] = tmp.id
            if "user_id" in data:  # user_id is an optional field
                if isinstance(data["user_id"], str):
                    tmp: [User | None] = User.query.filter_by(
                        person_id=data["user_id"]
                    ).first()
                    if not tmp:
                        raise DataValidationError(
                            MSG.USER_NOT_FOUND, MSG.LICENSE_PLATE_NOT_FOUND
                        )
                    data["user_id"] = tmp.id
        return data


class LicensePlateMoveManySchema(BaseMASchema):
    dest_location_id = LpMoveField(required=True, allowed_len=11)
    license_plate_ids = LicensePlateList(
        fields.Field(), required=True, validate=Length(min=1)
    )
    user_id = LpMoveField(required=False, allowed_len=17)

    def init(self, current_org):
        self.org = current_org

    @post_load
    def add_required_alt(self, data, *args, **kwargs):
        if data:
            if isinstance(data["dest_location_id"], str):
                tmp = (
                    Location.query.filter(
                        Location.beacon_id == data["dest_location_id"]
                    )
                    .filter(Location.organization_id == self.org.id)
                    .first()
                )
            else:
                tmp = Location.query.get(data["dest_location_id"])
            if not tmp or not tmp.active:
                raise DataValidationError(
                    "Location not found or no longer active",
                    MSG.LOCATION_NOT_FOUND
                )
            data["dest_location_id"] = tmp.id
            if "user_id" in data:
                if isinstance(data["user_id"], str):
                    tmp = User.query.filter_by(
                        person_id=data["user_id"]
                    ).first()
                    if not tmp:
                        raise DataValidationError(
                            MSG.USER_NOT_FOUND, MSG.USER_NOT_FOUND
                        )
                    data["user_id"] = tmp.id
        return data


class LicensePlateMoveAllSchema(BaseMASchema):
    dest_id = ma.Integer(required=True)
    source_id = ma.Integer(required=True)


class LicensePlateMadeItRequestSchema(BaseSQLAlchemyAutoSchema):
    # lp_ids = ma.String(required=True, many=True)
    id = ma.Int(dump_only=True)
    production_order_id = PRIDField(required=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True, required=False)  # read-only

    class Meta:
        exclude = ("updated_at",)
        model = LicensePlate
        sqla_session = db.session
        load_instance = False

        unknown = INCLUDE

    @pre_load
    def normalize(self, data, *args, **kwargs):
        if not data:
            return
        if 'person_id' in data and 'user_id' not in data:
            data['user_id'] = data['person_id'].split('/')[-1]
        if 'license_plate' in data and isinstance(data['license_plate'], str):
            data['lp_id'] = data['license_plate'].split('/')[-1]
        if 'Id' in data:
            data['external_serial_number'] = data['Id']
        return data


class LicensePlateMadeManyRequestSchema(BaseMASchema):
    ''' This is a schema for license plate made many request '''

    lp_ids = ma.List(ma.String(required=True))
    production_order_id = PRIDField(required=True)
    product_id = ma.Integer(required=False)
    message = ma.String(required=False)
    quantity = ma.Integer(required=True)


class LicensePlateMadeManyOrderRequestSchema(BaseSQLAlchemyAutoSchema):
    license_plates = fields.List(
        fields.Nested(LicensePlateMadeItRequestSchema(
            exclude=('production_order_id',)
        ))
    )


class LicensePlateProtoDumpSchema(BaseMASchema):
    id = ma.String()
    SONUM = ma.Int()
    JobID = ma.Int()
    JobName = ma.String()
    ItemNum = ma.Int()
    Image = ma.String()
    Index = ma.String()
    PART_NUMBER = ma.String()
    person_ID = ma.String()
    license_plate = ma.String()


class LicensePlateWrapSchema(BaseMASchema):
    location_id = LpMoveField(allowed_len=11, required=True)
    user_id = LpMoveField(allowed_len=17, required=False)


class LicensePlateRequestCycleCountSchema(BaseMASchema):
    license_plate_id = LpMoveField(allowed_len=25, required=True)

    @post_load
    def add_required_alt(self, data, *args, **kwargs):
        if data:
            if isinstance(data["license_plate_id"], str):
                tmp = (
                    LicensePlate.query.filter(
                        LicensePlate.lp_id == data["license_plate_id"]
                    ).first()
                )
            else:
                tmp = LicensePlate.query.get(data["license_plate_id"])
            stale = [
                LicensePlateStatusEnum.RETIRED,
                LicensePlateStatusEnum.DELETED
            ]
            if not tmp or tmp.status in stale:
                raise DataValidationError(
                    "LicensePlate not found or no longer active",
                    MSG.LICENSE_PLATE_NOT_FOUND
                )
            data["license_plate_id"] = tmp.id
        return data

# class LicensePlateMadeManyRequestSchema(BaseMASchema):
#     lp_ids = ma.String(required=True, many=True)
#     product_id = ma.Integer(required=True)
#     quantity = ma.Integer(required=False, default=1)
#     location_id = ma.Integer(required=True)


#     # lp_id = ma.Int(dump_only=True)
#     # lp_ids = ma.Nested(
#     #     ma.Int,
#     #     many=True,
#     # )

#     # id = ma.Int(dump_only=True)
#     # created_at = ma.String(dump_only=True)  # read-only
#     # organization_id = ma.Integer(
#           dump_only=True, required=False
#       )  # read-only
#     # product = fields.Nested("ProductSchema", only=("part_number",))

#     # class Meta:
#     #     exclude = ("updated_at",)
#     #     model = LicensePlate
#     #     sqla_session = db.session
#     #     load_instance = True
#     #     include_relationships = True
#     #     include_fk = True
