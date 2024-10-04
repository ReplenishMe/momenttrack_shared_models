import enum

from ..model_mixins import BelongsToOrgMixin, IdMixin, TimestampMixin
from ...extensions import db


class ShoppingListStatus(enum.Enum):
    """List of statuses of shopping list"""

    ADDED = "added"
    EXPORTED = "exported"
    DELETED = "deleted"


class ShoppingList(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    """venndor details"""

    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    product_id = db.Column(db.Integer(), db.ForeignKey("product.id"), nullable=False)
    bin_id = db.Column(db.Integer(), db.ForeignKey("bin.id"), nullable=False)
    quantity = db.Column(db.Float())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    organization_id = db.Column(
        db.Integer, db.ForeignKey("organization.id"), nullable=False
    )
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendor.id"))

    # activity_id = db.Column(db.Integer(), db.ForeignKey("activity.id"))

    # status = db.Column(db.Boolean(), nullable=False, server_default="0")
    # status =  db.Column(db.Enum(ShoppingListStatus), nullable=False, default=ShoppingListStatus.ADDED)
    status = db.Column(
        db.String(63),
        nullable=False,
        default=ShoppingListStatus.ADDED.value,
        server_default=ShoppingListStatus.ADDED.value,
    )

    # relations
    location = db.relationship("Location", foreign_keys="ShoppingList.location_id")
    product = db.relationship("Product", foreign_keys="ShoppingList.product_id")
    bin = db.relationship("Bin", foreign_keys="ShoppingList.bin_id")
    vendor = db.relationship("Vendor", foreign_keys="ShoppingList.vendor_id")
    user = db.relationship("User", foreign_keys="ShoppingList.user_id")
