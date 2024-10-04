from json import dumps as json_dumps
from json import loads as json_loads

from ..extensions import db
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.types import TypeDecorator


class PseudoJSON(TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return value

        return json_dumps(value)

    def process_result_value(self, value, dialect):
        if not value:
            return value
        return json_loads(value)


class MutableDict(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutableDict."

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."

        dict.__delitem__(self, key)
        self.changed()


class MutableList(Mutable, list):
    def append(self, value):
        list.append(self, value)
        self.changed()

    def remove(self, value):
        list.remove(self, value)
        self.changed()

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value
