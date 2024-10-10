import marshmallow.fields as ma

from momenttrack_shared_models.core.schemas._base import BaseMASchema, BaseSQLAlchemyAutoSchema
from momenttrack_shared_models.core.schemas._validators import validate_password
from momenttrack_shared_models.core.database.models import User
from momenttrack_shared_models.core.extensions import db


class UserSchema(BaseSQLAlchemyAutoSchema):
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


class AddUserSchema(BaseSQLAlchemyAutoSchema):
    password = ma.String(required=False, validate=[validate_password])

    class Meta:
        exclude = (
            "id",
            "person_id",
            "confirmed_at",
            "organization_id",
            "parent_user_id",
            "created_at",
            "updated_at",
        )
        model = User
        sqla_session = db.session
        load_instance = True
        # include_relationships = True
        include_fk = True


class InviteUserSchema(BaseMASchema):
    email = ma.Email(required=True)


class ChangePasswordSchema(BaseMASchema):
    password = ma.String(required=True, validate=[validate_password])


class ChangeRoleSchema(BaseMASchema):
    role_ids = ma.List(ma.Integer(), required=True)


class UserActivityReportSchema(BaseMASchema):
    activity_id = ma.Int(dump_only=True)
    first_name = ma.String(dump_only=True)
    last_name = ma.String(dump_only=True)
    user_id = ma.Int(dump_only=True)
    user_qr = ma.String(dump_only=True)
    production_order_id = ma.Int(dump_only=True)
    production_order_qr = ma.String(dump_only=True)
    production_order_internal_work_order = ma.String(dump_only=True)
    part_number = ma.String(dump_only=True)
    quantity = ma.Int(dump_only=True)
    created_at = ma.String(dump_only=True)
    organization_id = ma.Integer(required=False)
    activity_type = ma.String(dump_only=True)
    time_difference_in_seconds = ma.Int(dump_only=True)
    time_difference_in_minutes = ma.Int(dump_only=True)
    time_difference_in_hours = ma.Int(dump_only=True)
