import marshmallow.fields as ma

from momenttrack_shared_models.core.schemas._base import BaseMASchema
from momenttrack_shared_models.core.schemas.user_schema import UserSchema


class CeleryTaskResponseSchema(BaseMASchema):
    task_id = ma.String(required=True)


class NullSchema(BaseMASchema):
    pass


class UserCommentsSchema(BaseMASchema):
    message = ma.String(required=True)


class ActivityLogsSchema(BaseMASchema):
    # user_id = ma.Integer(required=True)
    user = ma.Nested(
        UserSchema,
        dump_only=True,
        only=["id", "person_id", "first_name"]
    )
    # activity_type = ma.String(required=True)
    message = ma.String(required=True)
    activity = ma.String(required=True)
    created_at = ma.DateTime(required=True)
    meta = ma.Raw(required=True)
