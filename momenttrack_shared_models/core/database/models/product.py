from ..model_mixins import BelongsToOrgMixin, IdMixin, TimestampMixin
from ...extensions import db
from ...utils import generate_token
from sqlalchemy.orm import validates


class Product(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    """item details"""

    __table_args__ = (
        db.UniqueConstraint("organization_id", "part_number"),
        db.UniqueConstraint(
            "organization_id", "preferred_vendor_id", "preferred_vendor_part_number"
        ),  # In an org, we can't same vendor & same partnumber combinations for any product.
    )

    part_number = db.Column(
        db.String(31), default=lambda: generate_token(length=31, upper_case_only=True)
    )
    name = db.Column(db.String(127), nullable=False)
    description = db.Column(db.String(255), default=None)
    organization_id = db.Column(
        db.Integer(), db.ForeignKey("organization.id"), nullable=False
    )
    preferred_vendor_id = db.Column(
        db.Integer(), db.ForeignKey("vendor.id"), server_default=None
    )
    preferred_vendor_part_number = db.Column(db.String(50))
    erp_part_number = db.Column(db.String(50))
    uom = db.Column(db.String(31))
    is_external = db.Column(
        db.Boolean(),
        nullable=True,
        default=False,
        server_default="false",
        comment="Whether the product is external to momenttrack (no tracking will be available for this)",
    )
    active = db.Column(db.Boolean(), nullable=False, default=True)

    # relations
    preferred_vendor = db.relationship(
        "Vendor", foreign_keys="Product.preferred_vendor_id"
    )

    license_plates = db.relationship("LicensePlate", backref="product", lazy="dynamic")

    @validates("part_number")
    def convert_upper(self, key, value):
        return value.upper()

    @classmethod
    def get_by_part_number_and_org(cls, part_number, org):
        part_number = part_number.upper()
        return cls.get_by_org(org).filter(cls.part_number == part_number).first()

    @classmethod
    def get_by_preferred_vendor_id_and_org(cls, preferred_vendor_id, org):
        return (
            cls.get_by_org(org)
            .filter(cls.preferred_vendor_id == preferred_vendor_id)
            .first()
        )
