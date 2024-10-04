from datetime import datetime

from ..model_mixins import BelongsToOrgMixin, IdMixin
from ...extensions import db
from ...utils import SerializableEnum


class ActivityTypeEnum(SerializableEnum):
    """activity types"""

    SHOPPINGLIST_REORDER = "SHOPPINGLIST_REORDER"
    # BIN_RELOCATE = "BIN_RELOCATE"
    CHANGE_TRACK = "CHANGE_TRACK"
    COMMENT = "COMMENT"
    LICENSE_PLATE_MOVE = "LICENSE_PLATE_MOVE"
    LICENSE_PLATE_MADEIT = "LICENSE_PLATE_MADEIT"
    LICENSE_PLATE_DEDUCT = "LICENSE_PLATE_DEDUCT"


class Activity(db.BaseModel, IdMixin, BelongsToOrgMixin):
    """Activity details"""

    model_name = db.Column(db.String(31), comment="Model/table name")
    model_id = db.Column(db.Integer(), comment="model's primary key")
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    loggedin_user_id = db.Column(
        db.Integer(), db.ForeignKey("user.id"), nullable=True
    )  # @TODO make if non-nullable
    organization_id = db.Column(
        db.Integer(), db.ForeignKey("organization.id"), nullable=False
    )
    message = db.Column(db.String(512), comment="user notes")
    activity_type = db.Column(
        db.Enum(ActivityTypeEnum, native_enum=True, length=31), nullable=True
    )
    # activity_type_id = db.Column(db.Integer(), db.ForeignKey("activity_type.id"))
    ip_address = db.Column(db.String(45))
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
