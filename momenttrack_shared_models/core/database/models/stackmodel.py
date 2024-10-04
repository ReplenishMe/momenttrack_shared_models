from ..model_mixins import BelongsToOrgMixin, IdMixin, TimestampMixin
from ...extensions import db
from ...utils import AppResponse, generate_token
from ...utils import SerializableEnum
from sqlalchemy.orm import validates
from ..models import LicensePlate


class StackStatusEnum(SerializableEnum):
    OPEN = "open"
    CLOSED = "closed"


class Stack(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    """Stack Model table"""
    stack_id = db.Column(
        db.String(63), nullable=False, unique=True, default=lambda: generate_token(25)
    )
    part_number = db.Column(db.String(63), nullable=False)
    production_order_id = db.Column(db.String(63), nullable=False)
    status = db.Column(
        db.Enum(StackStatusEnum, native_enum=True, length=31),
        nullable=False,
        default=StackStatusEnum.OPEN,
    )
    item_count = db.Column(db.Integer())
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    org_id = db.Column(db.Integer, db.ForeignKey("organization.id"), nullable=True)

    @classmethod
    def get_by_lp_id_and_org(cls, stack_id, fetch_all=False, session=None):
        if session:
            lp = cls.query.with_session(session).filter(cls.stack_id == stack_id)
        else:
            lp = cls.query.filter(cls.stack_id == stack_id)
        if fetch_all:
            return lp.all()
        return lp.first()

    @classmethod
    def get_loc_id_by_stack_id_and_org(cls, stack_id, fetch_all=False, session=None):
        if session:
            lp = cls.query.with_session(session).filter(cls.stack_id == stack_id)
        else:
            lp = cls.query.filter(cls.stack_id == stack_id)
        if fetch_all:
            return lp.all()
        return lp.first().location_id

    @classmethod
    def get_lp_list_or_none(cls, stack_id, fetch_all=False, session=None):
        if session:
            stack = cls.query.with_session(session).filter(cls.stack_id == stack_id).first()
        else:
            stack = cls.query.filter(cls.stack_id == stack_id).first()

        if stack:
            license_plates = LicensePlate.query.filter(LicensePlate.location_id == stack.location_id).all()
            return [lp.id for lp in license_plates] if license_plates else None

        return None

    @classmethod
    def get_by_org(cls, org_id, session=None):
        if session:
            lp = cls.query.with_session(session).filter(cls.org_id == org_id).order_by(cls.created_at.desc())
        else:
            lp = cls.query.filter(cls.org_id == org_id).order_by(cls.created_at.desc())

        return lp.all()
