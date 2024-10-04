import itertools
from enum import Enum
from functools import reduce

from ..datatypes import MutableList
from ..model_mixins import BelongsToOrgMixin, IdMixin, TimestampMixin
from .role import Role
from ...extensions import db, pwd_context
from ...utils import (
    generate_token,
    SerializableEnum
)
from flask_login import AnonymousUserMixin, UserMixin

# from flask_continuum import VersioningMixin
from sqlalchemy.dialects import postgresql


class UserStatusEnum(SerializableEnum):
    UNCONFIRMED = "UNCONFIRMED"
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"

class UserShiftEnum(SerializableEnum):
    NA = "NA"
    MORNING = "MORNING"
    DAY = "DAY"
    EVENING = "EVENING"
class PermissionsCheckMixin(object):
    def has_permission(self, permission):
        if isinstance(permission, (Enum,)):
            permission = permission.value
        return self.has_permissions((permission,))

    def has_permissions(self, permissions):
        has_permissions = reduce(
            lambda a, b: a and b,
            [permission in self.permissions for permission in permissions],
            True,
        )

        return has_permissions


class User(
    db.BaseModel,
    IdMixin,
    TimestampMixin,
    UserMixin,
    BelongsToOrgMixin,
    PermissionsCheckMixin,
):
    """User auth & profile details"""

    __table_args__ = (db.UniqueConstraint("organization_id", "email"),)

    # Auth info
    person_id = db.Column(db.CHAR(17), unique=True, default=lambda: generate_token(17))
    email = db.Column(
        db.String(254),
        nullable=False,
        unique=True,
        comment="https://stackoverflow.com/a/574698",
    )
    confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default="")
    # active = db.Column(db.Boolean(), nullable=False, default=False)
    status = db.Column(
        db.Enum(UserStatusEnum, native_enum=True, length=31),
        nullable=False,
        default=UserStatusEnum.UNCONFIRMED,
    )

    # if user signs up, using oauth
    # oauth_id = db.Column(db.String(), nullable=True, unique=True, index=True)

    # # tracking
    # last_login_at = db.Column(db.DateTime())
    # current_login_at = db.Column(db.DateTime())
    # last_login_ip = db.Column(db.String(100))
    # current_login_ip = db.Column(db.String(100))
    # login_count = db.Column(db.Integer)

    # Profile info
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    phone = db.Column(db.String(30))
    organization_id = db.Column(
        db.Integer(), db.ForeignKey("organization.id"), nullable=False
    )
    parent_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    preferred_printer_id = db.Column(
        db.Integer(), db.ForeignKey("printer.id"), server_default=None
    )
    shift=db.Column(db.Enum(UserShiftEnum, native_enum=True, length=10),
        default=UserShiftEnum.NA,)
    role_ids = db.Column(
        "roles", MutableList.as_mutable(postgresql.ARRAY(db.Integer)), nullable=True
    )

    # for flask-login
    @property
    def is_active(self):
        return self.status == UserStatusEnum.ACTIVE

    @property
    def is_inactive(self):
        return not self.is_active

    # for flask-login
    def get_id(self):
        return str(self.id)

    # for permissions mixin
    @property
    def permissions(self):
        if not self.role_ids:
            return []

        # TODO: this should be cached.
        return list(
            itertools.chain(
                *[
                    role.permissions
                    for role in Role.query.filter(Role.id.in_(self.role_ids))
                ]
            )
        )

    @classmethod
    def get_by_person_id_and_org(cls, person_id, org, session=None):
        # person_id = person_id.upper()
        if session:
            return (
                cls.get_by_org(org, session=session)
                .filter(cls.person_id == person_id)
                .first()
            )
        return cls.get_by_org(org).filter(cls.person_id == person_id).first()

    @classmethod
    def get_by_id(cls, _id, session=None):
        if session:
            return cls.query.with_session(session).filter(cls.id == _id).first()
        return cls.query.filter(cls.id == _id).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(cls.email == email).first()

    @classmethod
    def get_by_email_and_org(cls, email, org):
        return cls.get_by_org(org).filter(cls.email == email).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter(cls.email == email)

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return self.password and pwd_context.verify(password, self.password)

    def has_access(self, obj, access_type):
        pass

    def __repr__(self):
        return "User<id={}, email={}>".format(self.id, self.email)


class AnonymousUser(AnonymousUserMixin, PermissionsCheckMixin):
    id = -1

    @property
    def permissions(self):
        return []

    def is_api_user(self):
        return False
