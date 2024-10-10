import marshmallow.fields as ma

from momenttrack_shared_models.core.schemas._base import BaseMASchema, BaseSQLAlchemyAutoSchema
from momenttrack_shared_models.core.database.models import LicensePlate
from momenttrack_shared_models.core.extensions import db
from marshmallow import validate


class EverythingReportSchema(BaseSQLAlchemyAutoSchema):
    id = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)  # read-only

    beacon_id = ma.String()  # external
    location_name = ma.String()  # external
    location_width = ma.Float()  # external
    location_height = ma.Float()  # external
    location_depth = ma.Float()  # external
    category = ma.String()  # external

    part_number = ma.String()  # external
    description = ma.String()  # external
    intake_date = ma.String()  # external
    who_moved_last = ma.String()  # external
    when_last_movement = ma.String()  # external
    last_interaction = ma.String()  # external

    class Meta:
        exclude = (
            "updated_at",
            "parent_license_plate_id",
            "is_consumer_facing",
            "redirect_url",
            "license_plate_move",
            "location",
            "product",
        )
        model = LicensePlate
        sqla_session = db.session
        load_instance = True
        include_relationships = True
        include_fk = True


class RequestReportSchema(BaseMASchema):
    email = ma.String(required=True, validate=validate.Email())
