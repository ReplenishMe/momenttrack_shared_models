from ..model_mixins import BelongsToOrgMixin, IdMixin, TimestampMixin
from ...extensions import db


class BinFamily(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    """bin family details"""

    product_id = db.Column(db.Integer(), db.ForeignKey("product.id"), nullable=False)
    default_quantity = db.Column(db.Float())
    location_id = db.Column(db.Integer(), db.ForeignKey("location.id"), nullable=False)
    preferred_vendor_id = db.Column(
        db.Integer(), db.ForeignKey("vendor.id"), server_default=None
    )
    organization_id = db.Column(
        db.Integer(), db.ForeignKey("organization.id"), nullable=False
    )
    active = db.Column(db.Boolean(), nullable=False, default=True)

    # relations
    preferred_vendor = db.relationship(
        "Vendor", foreign_keys="BinFamily.preferred_vendor_id"
    )
    location = db.relationship("Location", foreign_keys="BinFamily.location_id")
    product = db.relationship("Product", foreign_keys="BinFamily.product_id")
