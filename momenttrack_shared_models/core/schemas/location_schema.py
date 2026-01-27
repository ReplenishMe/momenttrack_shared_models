from datetime import datetime
import marshmallow.fields as ma
from sqlalchemy import select, desc

from momenttrack_shared_models.core.schemas import (
    LicensePlateSchema,
    ProductSchema, LineGraphDataSchema,
    LocationPartNoTotalsSchema
)
from momenttrack_shared_models.core.schemas._base import (
    BaseSQLAlchemyAutoSchema,
    BaseMASchema
)
from momenttrack_shared_models.core.database.models import (
    LicensePlateMove,
    Location, LicensePlate,
    LineGraphData, LocationPartNoTotals
)
from momenttrack_shared_models.core.extensions import db
from marshmallow import (
    pre_dump, pre_load,
    post_dump, fields
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
        load_instance = True
        include_relationships = True
        include_fk = True

    @pre_dump
    def normalize_date(self, obj, **kwargs):
        try:
            if obj:
                if isinstance(obj.created_at, str):
                    obj.created_at = datetime.strptime(obj.created_at, "%Y-%m-%d %H:%M:%S.%f")
                if isinstance(obj.created_at, datetime):
                    obj.created_at = obj.created_at.strftime(
                        "%Y-%m-%d %H:%M:%S.%f"
                    )
                if obj.left_at:
                    if isinstance(obj.left_at, str):
                        obj.left_at = datetime.strptime(obj.left_at, "%Y-%m-%d %H:%M:%S.%f")
                    if isinstance(obj.left_at, datetime):
                        obj.left_at = obj.left_at.strftime(
                            "%Y-%m-%d %H:%M:%S.%f"
                        )
            return obj
        except Exception as e:
            print(e)
            print(obj.id, type(obj.left_at), type(obj.created_at))

    @post_dump
    def data_check(self, data, **kwargs):
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


class LocReportSchema(BaseSQLAlchemyAutoSchema):
    class Meta:
        # exclude = ("updated_at",)
        model = Location
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True
        fields = (
            'beacon_id', 'active', 'lp_qty', 'created_at',
            'line_graph_data', 'name', 'location_partno_totals',
            'oldest_lp', 'average_duration', 'id'
        )

    line_graph_data = fields.Method(serialize='get_line_graph_data')
    location_partno_totals = fields.Method(
        serialize='get_loc_part_no_data'
    )
    oldest_lp = fields.Method(serialize='get_oldest_lp')

    def get_oldest_lp(self, obj):
        stmt = select(LicensePlateMove).where(
            LicensePlateMove.dest_location_id == obj.id
        ).order_by(desc(LicensePlateMove.created_at)).limit(1)
        lp_move = db.session.scalar(stmt)
        if lp_move:
            lp = db.session.scalar(
                select(LicensePlate).where(
                    LicensePlate.id == lp_move.license_plate_id
                )
            )
            return LicensePlateSchema(
                only=('lp_id', 'product')
            ).dump(lp)
        return {}

    def get_line_graph_data(self, obj):
        stmt = select(LineGraphData).where(
            LineGraphData.location_id == obj.id
        )
        res = db.session.scalars(stmt)
        return LineGraphDataSchema(
            many=True,
            exclude=('organization_id',)
        ).dump(res)

    def get_loc_part_no_data(self, obj):
        stmt = select(LocationPartNoTotals).where(
            LocationPartNoTotals.location_id == obj.id
        )
        res = db.session.scalars(stmt)
        return LocationPartNoTotalsSchema(
            many=True,
            exclude=('organization_id',)
        ).dump(res)
