import marshmallow_sqlalchemy.schema as ma
from marshmallow import pre_load

from momenttrack_shared_models.core.utils import DataValidationError

# A good tutorial on using marshmallow:
#  https://www.kimsereylam.com/python/2019/10/25/serialization-with-marshmallow.html
#


def _parse_ma_error(exc, data, **kwargs):
    # format & custom the messages
    message = ""
    for key, val in exc.messages.items():
        err = val[0]
        if "Missing data" in err:
            message = f"{key}: Missing data for required field"
        else:
            message = f"{key}: {err}"
        break

    return message


class BaseMASchema(ma.Schema):
    def handle_error(self, exc, data, **kwargs):
        """Log and raise our custom exception when (de)serialization fails."""
        message = _parse_ma_error(exc, data, **kwargs)
        raise DataValidationError(
            message=message,
            errors=exc.messages,
            data=data
        )

    @pre_load
    def emails_should_be_lower_case(self, data, many, partial):
        """Convert all `email` fields to lower case"""
        if data and "email" in data:
            data["email"] = data["email"].lower()

        return data


class BaseSQLAlchemyAutoSchema(ma.SQLAlchemyAutoSchema):
    def handle_error(self, exc, data, **kwargs):
        """Log and raise our custom exception when (de)serialization fails."""
        message = _parse_ma_error(exc, data, **kwargs)

        raise DataValidationError(
            message=message,
            errors=exc.messages,
            data=data
        )

    @pre_load
    def remove_skip_values(self, data, many, partial):
        """Treat nulls & empty strings are undefined

        As per these guidelines:
         https://google.github.io/styleguide/jsoncstyleguide.xml#Empty/Null_Property_Values
        """
        if not data:
            return data

        SKIP_VALUES = ["", None]
        return {
            key: val for key, val in data.items() if val not in SKIP_VALUES
        }

    @pre_load
    def emails_should_be_lower_case(self, data, many, partial):
        """Convert all `email` fields to lower case"""
        if data and "email" in data:
            data["email"] = data["email"].lower()

        return data
