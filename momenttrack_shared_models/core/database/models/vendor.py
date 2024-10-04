from ..model_mixins import BelongsToOrgMixin, IdMixin, TimestampMixin
from ...extensions import db


class Vendor(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    """venndor details"""

    __table_args__ = (db.UniqueConstraint("organization_id", "name"),)

    organization_id = db.Column(
        db.Integer(), db.ForeignKey("organization.id"), nullable=False
    )
    name = db.Column(db.String(50), nullable=False)
    erp_number = db.Column(db.String(50))
    active = db.Column(db.Boolean(), nullable=False, default=True)

    @classmethod
    def get_by_name_and_org(cls, name, org):
        return cls.get_by_org(org).filter(cls.name == name).first()
