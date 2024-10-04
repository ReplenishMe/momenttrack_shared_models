from ..model_mixins import BelongsToOrgMixin, IdMixin, TimestampMixin
from ...extensions import db
from sqlalchemy.dialects import postgresql


class Role(db.BaseModel, IdMixin, BelongsToOrgMixin, TimestampMixin):
    __table_args__ = (db.UniqueConstraint("organization_id", "name"),)

    DEFAULT_PERMISSIONS = ["view_profile"]

    BUILTIN_GROUP = "builtin"
    USERDEFINED_GROUP = "userdefined"

    organization_id = db.Column(
        db.Integer(), db.ForeignKey("organization.id"), nullable=False
    )

    role_type = db.Column(db.String(255), default=USERDEFINED_GROUP)

    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255))
    permissions = db.Column(
        postgresql.ARRAY(db.String(255)), default=DEFAULT_PERMISSIONS
    )

    @classmethod
    def lookup(cls, name):
        return cls.query.filter_by(name=name).one_or_none()

    @classmethod
    def all(cls, org):
        return cls.query.filter(cls.org == org)

    @classmethod
    def members(cls, group_id):
        return User.query.filter(User.group_ids.any(group_id))

    @classmethod
    def find_by_name(cls, org, group_names):
        result = cls.query.filter(cls.org == org, cls.name.in_(group_names))
        return list(result)
