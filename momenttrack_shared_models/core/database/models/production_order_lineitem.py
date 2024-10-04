from ..model_mixins import BelongsToOrgMixin, IdMixin, TimestampMixin
from ...extensions import db
from ...utils import SerializableEnum


class ProductionOrderLineitemStatusEnum(SerializableEnum):
    CREATED = "CREATED"
    DRAFT = "DRAFT"
    ONHOLD = "ONHOLD"
    COMPLETE = "COMPLETE"
    DELETED = "DELETED"


class ProductionOrderLineitem(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    """Production Order - line items table"""

    # __table_args__ = (
    #     db.UniqueConstraint('organization_id', 'name'),
    # )

    production_order_id = db.Column(db.Integer, db.ForeignKey("production_order.id"))
    # product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    license_plate_id = db.Column(db.Integer, db.ForeignKey("license_plate.id"))
    license_plate_move_id = db.Column(
        db.Integer, db.ForeignKey("license_plate_move.id")
    )
    organization_id = db.Column(
        db.Integer(), db.ForeignKey("organization.id"), nullable=False
    )
    qty = db.Column(db.Float())
    # status = db.Column(db.String(31), nullable=False, default="CREATED") # created/draft/complete/incomplete
    status = db.Column(
        db.Enum(ProductionOrderLineitemStatusEnum, native_enum=True, length=31),
        nullable=False,
        default=ProductionOrderLineitemStatusEnum.CREATED,
    )

    # product = db.relationship("Product", backref="production_order_lineitem", lazy="joined")
