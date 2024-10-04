from datetime import datetime

from ..extensions import db
from sqlalchemy.ext.declarative import declared_attr


class IdMixin:
    """Add auto increment column to table"""

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    @classmethod
    def get(cls, id_):
        return cls.query.get(id_)


class TimestampMixin:
    """Adds created_at & updated_at columns to the table

    Using declared_attrs to add columns to end. Ref: https://stackoverflow.com/a/4013184/2528464
    """

    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    @declared_attr
    def updated_at(cls):
        return db.Column(db.DateTime(), onupdate=datetime.utcnow)


class BelongsToOrgMixin(object):
    @classmethod
    def get_by_org(cls, org, session=None):
        if session:
            if isinstance(org, int):
                return cls.query.with_session(session).filter(
                    cls.organization_id == org
                )
            else:
                return cls.query.with_session(session).filter(
                    cls.organization_id == org.id
                )
        else:
            if isinstance(org, int):
                return cls.query.filter(cls.organization_id == org)
            else:
                return cls.query.filter(cls.organization_id == org.id)

    @classmethod
    def get_by_org_id(cls, org_id, session=None):
        if session:
            return cls.query.with_session(session).filter(cls.organization_id == org_id)
        return cls.query.filter(cls.organization_id == org_id)

    @classmethod
    def get_by_id_and_org(cls, object_id, org, org_cls=None, session=None):
        if session:
            query = cls.query.with_session(session).filter(cls.id == object_id)
        else:
            query = cls.query.filter(cls.id == object_id)
        if org_cls is None:
            if isinstance(org, int):
                query = query.filter(cls.organization_id == org)
            else:
                query = query.filter(cls.organization_id == org.id)
        else:
            query = query.join(org_cls).filter(org_cls.org == org)
        return query.first()

    def __repr__(self):
        return f"{self.organization_id} > {self.__class__.__name__}"
    

    @classmethod
    def get_by_id(cls, object_id, org_cls=None, session=None):
        if session:
            query = cls.query.with_session(session).filter(cls.id == object_id)
        else:
            query = cls.query.filter(cls.id == object_id)
        
        return query.first()



