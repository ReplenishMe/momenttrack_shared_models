from ..model_mixins import (
    BelongsToOrgMixin,
    IdMixin,
    TimestampMixin
)
from ...extensions import db
from ...utils import (
    generate_token,
    SerializableEnum
)


class ContainerMoveStatusEnum(SerializableEnum):
    CREATED = "CREATED"
    DELETED = "DELETED"


class Container(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    container_id = db.Column(
        db.String(),
        nullable=False,
        unique=True,
        index=True,
        default=lambda: generate_token(25)
    )
    redirect_url = db.Column(db.String())
    quantity = db.Column(db.Integer, nullable=False)

    location_id = db.Column(
        db.Integer,
        db.ForeignKey('location.id'),
        nullable=False,
        index=True
    )
    organization_id = db.Column(
        db.Integer,
        db.ForeignKey('organization.id'),
        nullable=False,
        index=True
    )
    parent_container_id = db.Column(db.Integer)
    location = db.relationship("Location")


class ContainerMove(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    container_id = db.Column(
        db.Integer,
        db.ForeignKey('container.id'),
        nullable=False,
        index=True
    )
    organization_id = db.Column(
        db.Integer(),
        db.ForeignKey("organization.id"),
        nullable=False,
        index=True
    )
    src_location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    dest_location_id = db.Column(
        db.Integer,
        db.ForeignKey("location.id"),
        index=True
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    activity_id = db.Column(db.Integer(), db.ForeignKey("activity.id"))
    left_at = db.Column(db.DateTime())
    status = db.Column(
        db.Enum(ContainerMoveStatusEnum, native_enum=True, length=31),
        nullable=False,
        default=ContainerMoveStatusEnum.CREATED,
    )
    user = db.relationship("User", backref="container_move", lazy="joined")
