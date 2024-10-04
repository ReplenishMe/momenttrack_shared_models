from datetime import datetime

from ..model_mixins import BelongsToOrgMixin, IdMixin
from ...extensions import db
from ...utils import SerializableEnum


class ActivityChangeTrackFieldTypeEnum(SerializableEnum):
    """field types"""

    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    DATETIME = "DATETIME"


class ActivityChangeTrack(db.BaseModel, IdMixin, BelongsToOrgMixin):
    """Activity details"""

    activity_id = db.Column(db.Integer(), db.ForeignKey("activity.id"))
    organization_id = db.Column(
        db.Integer(), db.ForeignKey("organization.id"), nullable=False
    )

    field_name = db.Column(db.String(31), comment="Column name")
    field_type = db.Column(
        db.Enum(ActivityChangeTrackFieldTypeEnum, native_enum=True, length=31),
        nullable=False,
        comment="column data type",
    )

    old_value_integer = db.Column(db.Integer(), nullable=True, default=None)
    old_value_float = db.Column(db.Float(), nullable=True, default=None)
    old_value_string = db.Column(db.String(255), nullable=True, default=None)
    old_value_datetime = db.Column(db.DateTime(), nullable=True, default=None)

    new_value_integer = db.Column(db.Integer(), nullable=True, default=None)
    new_value_float = db.Column(db.Float(), nullable=True, default=None)
    new_value_string = db.Column(db.String(255), nullable=True, default=None)
    new_value_datetime = db.Column(db.DateTime(), nullable=True, default=None)

    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
