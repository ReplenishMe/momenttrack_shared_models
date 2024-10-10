import marshmallow.fields as ma

from momenttrack_shared_models.core.schemas import (
    LicensePlateSchema,
    ProductSchema
)
from momenttrack_shared_models.core.schemas._base import (
    BaseSQLAlchemyAutoSchema,
    BaseMASchema
)
from momenttrack_shared_models.core.database.models import (
    LicensePlateMove,
    Location, LicensePlate
)
from momenttrack_shared_models.core.extensions import db
from marshmallow import (
    pre_dump, pre_load,
    post_dump
)


class LocationSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True, required=False)  # read-only

    class Meta:
        exclude = ("updated_at",)
        model = Location
        sqla_session = db.session
        load_instance = True
        # include_relationships = True
        include_fk = True

    @pre_load
    def check_enum_value(self, data, **kwargs):
        """intercepts 'unit' field in json and preformats it"""
        if data:
            if "unit" in data.keys():
                data["unit"] = data["unit"].upper()
            return data


class LicensePlateMoveLogsSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True, data_key="arrived_at")  # read-only
    left_at = ma.String()
    product = ma.Nested(
        ProductSchema(
            exclude=(
                "license_plate_move",
                "license_plates",
                "production_order"
            )
        ),
        dump_only=True,
    )
    user = ma.Nested("UserSchema", dump_only=True)
    license_plate = ma.Nested(
        LicensePlateSchema(
            only=(
                "lp_id",
                "quantity",
                "id",
                "external_serial_number",
                "product_id",
                "product",
            )
        ),
        dump_only=True,
    )

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

    @post_dump
    def data_check(self, data, *, session=None, **kwargs):
        if "lp_id" not in data["license_plate"]:
            data["license_plate"] = LicensePlateSchema().dump(
                LicensePlate.get_by_id_and_org(
                    data["license_plate_id"],
                    data["organization_id"]
                )
            )
        return data


class LocationReportEmailSchema(BaseMASchema):
    email = ma.String(required=True)
    location_id = ma.Integer(required=True)


class LocationReportSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only
    organization_id = ma.Integer(dump_only=True, required=False)  # read-only
    oldest_license_plate = ma.Nested(
        LicensePlateSchema(
            only=(
                "id", "lp_id",
                "product_id", "quantity",
                "product"
            )
        )
    )
    current_user = ma.Nested("UserSchema")
    license_plates = ma.Nested(
        LicensePlateSchema(
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
