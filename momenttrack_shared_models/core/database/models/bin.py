from ..model_mixins import BelongsToOrgMixin, IdMixin, TimestampMixin
from ...extensions import db


class Bin(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    """bin details"""

    __table_args__ = (db.UniqueConstraint("organization_id", "name"),)

    name = db.Column(db.String(36), nullable=False)
    bin_family_id = db.Column(
        db.Integer(), db.ForeignKey("bin_family.id"), nullable=False
    )
    organization_id = db.Column(
        db.Integer(), db.ForeignKey("organization.id"), nullable=False
    )
    active = db.Column(db.Boolean(), nullable=False, default=True)

    # relations
    bin_family = db.relationship("BinFamily", foreign_keys="Bin.bin_family_id")

    @classmethod
    def get_by_name_and_org(cls, name, org):
        return cls.get_by_org(org).filter(cls.name == name).first()
