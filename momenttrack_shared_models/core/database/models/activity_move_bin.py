from ..model_mixins import BelongsToOrgMixin, IdMixin
from ...extensions import db

# class ActivityType(enum.Enum):
#     """activity types"""
#     REORDER = "reorder"
#     BIN_RELOCATE = "BIN_RELOCATE"


class ActivityMoveBin(db.BaseModel, IdMixin, BelongsToOrgMixin):
    """Activity details"""

    organization_id = db.Column(
        db.Integer(), db.ForeignKey("organization.id"), nullable=False
    )
    activity_id = db.Column(db.Integer(), db.ForeignKey("activity.id"))
    bin_family_id = db.Column(db.Integer(), db.ForeignKey("bin_family.id"))
    prev_location_id = db.Column(db.Integer(), db.ForeignKey("location.id"))
    new_location_id = db.Column(db.Integer(), db.ForeignKey("location.id"))
