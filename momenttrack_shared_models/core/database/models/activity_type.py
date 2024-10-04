from ..model_mixins import IdMixin
from ...extensions import db


class ActivityType(db.BaseModel, IdMixin):
    """ActivityType details"""

    name = db.Column(db.String(128), nullable=False, unique=True)

    @classmethod
    def lookup(cls, name):
        return cls.query.filter(cls.name == name).first()
