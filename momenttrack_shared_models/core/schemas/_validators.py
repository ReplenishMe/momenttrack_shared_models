from marshmallow import ValidationError


def validate_password(value):
    if len(value) < 6:
        raise ValidationError("Password must be longer than 6 characters")
