from ..model_mixins import BelongsToOrgMixin, IdMixin, TimestampMixin
from ...extensions import db


class Printer(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    """printer details"""

    __table_args__ = (db.UniqueConstraint("organization_id", "name"),)

    name = db.Column(db.String(128))
    url = db.Column(db.String(255), unique=True)
    organization_id = db.Column(
        db.Integer(), db.ForeignKey("organization.id"), nullable=False
    )
    active = db.Column(db.Boolean(), nullable=False, default=True)

    users = db.relationship("User", backref="printer")

    @classmethod
    def get_by_name_and_org(cls, name, org):
        return cls.get_by_org(org).filter(cls.name == name).first()
