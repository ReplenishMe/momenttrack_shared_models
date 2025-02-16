from loguru import logger
from marshmallow import fields

from momenttrack_shared_models.core.database.models import Container
from momenttrack_shared_models.core.schemas._base import (
    BaseMASchema,
    BaseSQLAlchemyAutoSchema
)


class InvalidLengthError(Exception):
    pass


class ContainerMoveField(fields.Field):
    #: Default error messages.
    default_error_messages = {
        "invalid": "Not a valid 'LpMoveField' value.",
        "length": "Invalid length for field value",
    }

    def __init__(self, allowed_len=None, **kwargs):
        super().__init__(**kwargs)
        self.allowed_len = allowed_len

    def _verifyData(self, val):
        int_cond = isinstance(val, int)
        str_cond = isinstance(val, str)

        assert (int_cond or str_cond) == True

        if str_cond:
            try:
                assert len(val) == self.allowed_len
            except AssertionError:
                raise InvalidLengthError

        return val

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        try:
            return self._verifyData(value)
        except AssertionError as e:
            raise self.make_error("invalid")
            logger.error(e)
        except InvalidLengthError as e:
            raise self.make_error("length")
            logger.error(e)

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        try:
            return self._verifyData(value)
        except AssertionError as e:
            raise self.make_error("invalid")
            logger.error(e)
        except InvalidLengthError as e:
            raise self.make_error("length")
            logger.error(e)


class ContainerMoveSchema(BaseMASchema):
    container_id = ContainerMoveField(dump_only=True)
    dest_location_id = ContainerMoveField(dump_only=True)
    user_id = ContainerMoveField(dump_only=True)


class ContainerSchema(BaseSQLAlchemyAutoSchema):
    class Meta:
        model = Container
        include_relationships = True
        include_fk = True
