from ..model_mixins import BelongsToOrgMixin, IdMixin, TimestampMixin
from ...extensions import db
from ...utils import SerializableEnum


class PickLineitemStatusEnum(SerializableEnum):
    CREATED = "CREATED"
    DRAFT = "DRAFT"
    DONE = "DONE"
    DELETED = "DELETED"


class PickLineitem(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    """WMS: Pick - line items table"""

    # __table_args__ = (
    #     db.UniqueConstraint('organization_id', 'name'),
    # )

    pick_id = db.Column(db.Integer, db.ForeignKey("pick.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    license_plate_id = db.Column(db.Integer, db.ForeignKey("license_plate.id"))
    license_plate_move_id = db.Column(
        db.Integer, db.ForeignKey("license_plate_move.id")
    )
    organization_id = db.Column(
        db.Integer(), db.ForeignKey("organization.id"), nullable=False
    )
    requested_qty = db.Column(db.Float())
    fulfilled_qty = db.Column(db.Float(), default=0)
    # status = db.Column(db.String(31), nullable=False, default="CREATED") # created/draft/complete/incomplete
    status = db.Column(
        db.Enum(PickLineitemStatusEnum, native_enum=True, length=31),
        nullable=False,
        default=PickLineitemStatusEnum.CREATED,
    )

    product = db.relationship("Product", backref="pick_lineitem", lazy="joined")
