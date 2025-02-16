from ..model_mixins import BelongsToOrgMixin, IdMixin, TimestampMixin
from ...extensions import db
from ...utils import generate_token
from ...utils import SerializableEnum


from sqlalchemy.orm import validates
from sqlalchemy_json import mutable_json_type
from sqlalchemy.dialects.postgresql import JSONB

# from sqlalchemy.ext.hybrid import hybrid_property


class UnitTypeEnum(SerializableEnum):
    """unit field types"""

    FEET = "FEET"
    METER = "METER"
    INCHES = "INCHES"

    @classmethod
    def matchValue(cls, value):
        try:
            enum_member = cls[value] or cls[value.upper()]
            return True
        except KeyError:
            # return data validation error
            return False


class Location(db.BaseModel, IdMixin, TimestampMixin, BelongsToOrgMixin):
    """location table"""

    # __table_args__ = (
    #     db.UniqueConstraint('organization_id', 'name'),
    # )

    beacon_id = db.Column(
        db.String(11),
        default=lambda: generate_token(length=11, upper_case_only=True)
    )
    name = db.Column(db.String(63), nullable=False)
    parent_location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    location_type = db.Column(db.String(63))
    organization_id = db.Column(
        db.Integer(), db.ForeignKey("organization.id"), nullable=False
    )
    public_access = db.Column(db.Boolean(), nullable=False, default=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)
    lp_qty = db.Column(db.Integer(), nullable=False, default=0)
    logo_url = db.Column(db.String())
    width = db.Column(db.Float())
    height = db.Column(db.Float())
    depth = db.Column(db.Float())
    unit = db.Column(
        "unit",
        db.Enum(UnitTypeEnum),
        comment="unit column data type"
    )
    trigger = db.Column(
        mutable_json_type(
            dbtype=JSONB,
            nested=True
        )
    )

    license_plates = db.relationship(
        "LicensePlate",
        backref="location",
        lazy="dynamic"
    )
    containers = db.relationship("Container", back_populates='location')

    @validates("beacon_id")
    def convert_upper(self, key, value):
        return value.upper()

    @classmethod
    def get_by_beacon_id_and_org(cls, beacon_id, org):
        beacon_id = beacon_id.upper()
        return cls.get_by_org(org).filter(cls.beacon_id == beacon_id).first()

    @classmethod
    def get_by_id_and_org(cls, loc_id, org, session=None):
        return cls.get_by_org(org, session=session).filter(
            cls.id == loc_id
        ).first()

    @classmethod
    def get_by_name_and_org(cls, name, org):
        return cls.get_by_org(org).filter(cls.name == name).first()

    @property
    def is_active(self):
        return self.active

    @property
    def is_inactive(self):
        return not self.is_active

    # @hybrid_property
    # def unit(self):
    #     return self._unit

    # @unit.setter
    # def unit(self, value):
    #     new_enum_value = UnitTypeEnum.matchValue(value)
    #     if new_enum_value:
    #         self._unit = new_enum_value
    #     else:
    #         return AppResponse.error(
    #             message=f"unit of type {value} does not exit check spelling",
    #             code=400,
    #             errors=KeyError
    #         )

    @classmethod
    def get_system_location(cls, org_id, session=None):
        if session:
            loc = cls.get_by_org(org_id, session=session).filter(
                cls.name == "SYSTEM_LOCATION"
            ).first()
        else:
            loc = cls.get_by_org(org_id).filter(
                cls.name == "SYSTEM_LOCATION"
            ).first()
        if not loc:
            db.writer_session.add(
                cls(
                    name="SYSTEM_LOCATION",
                    organization_id=org_id,
                    location_type="system",
                )
            )
            # print(vars(db.writer_session.bind))
            db.writer_session.commit()
            loc = cls.get_by_org(org_id).filter(
                cls.name == "SYSTEM_LOCATION"
            ).first()
        return loc
