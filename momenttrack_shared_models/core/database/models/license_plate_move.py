from sqlalchemy import select

from ..models import User
from ..model_mixins import BelongsToOrgMixin, IdMixin, TimestampMixin
from ...extensions import db, open_client
from ...utils import generate_token
from ...utils import SerializableEnum


class LicensePlateMoveStatusEnum(SerializableEnum):
    CREATED = "CREATED"
    DELETED = "DELETED"


# class LicensePlateMoveTypeEnum(SerializableEnum):
#     SPLIT = "SPLIT"
#     TRANSFER = "TRANSFER"


class LicensePlateMove(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    """WMS: License plate move table"""

    # __table_args__ = (
    #     db.UniqueConstraint('organization_id', 'name'),
    # )

    trx_id = db.Column(
        db.String(63), nullable=False, unique=True, default=lambda: generate_token(25)
    )
    license_plate_id = db.Column(
        db.Integer, db.ForeignKey("license_plate.id"), nullable=False, index=True
    )
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)

    organization_id = db.Column(
        db.Integer(), db.ForeignKey("organization.id"), nullable=False, index=True
    )
    src_location_id = db.Column(db.Integer, db.ForeignKey("location.id"), index=True)
    dest_location_id = db.Column(db.Integer, db.ForeignKey("location.id"), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    activity_id = db.Column(db.Integer(), db.ForeignKey("activity.id"))
    left_at = db.Column(db.DateTime())

    # move_type = db.Column(
    #     db.Enum(LicensePlateMoveTypeEnum, native_enum=True, length=31), nullable=False
    # )

    status = db.Column(
        db.Enum(LicensePlateMoveStatusEnum, native_enum=True, length=31),
        nullable=False,
        default=LicensePlateMoveStatusEnum.CREATED,
    )

    product = db.relationship("Product", backref="license_plate_move", lazy="joined")
    user = db.relationship("User", backref="license_plate_move", lazy="joined")
    license_plate = db.relationship(
        "LicensePlate", backref="license_plate_move", lazy="joined"
    )

    def update_associated_report(self, last_interaction_time, lp_report, session):
        from momenttrack_shared_models.core.database.models import EverythingReport
        lp_id = self.license_plate.lp_id
        user: User = session.scalar(
            select(User).where(User.id == self.user_id)
        )
        payload = {
            "who_moved_last": user.person_id,
            "when_last_movement": self.created_at,
            "last_interaction": last_interaction_time,
            **lp_report
        }

        report = session.scalar(
            select(EverythingReport).where(
                EverythingReport.lp_id == lp_id
            )
        )
        for k, v in payload.items():
            setattr(report, k, v)
