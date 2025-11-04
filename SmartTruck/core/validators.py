'''
    Custom validator functions or classes should be defined here
'''

## django lib
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

## django extensions
from ulid_django.converters import ULIDConverter

## python libs
from ulid import ULID


def validate_not_whitespace_only(value):
    '''
        Used in models that save a CharField which must not be an empty string.
    '''
    if not value.strip():
        print("Value cannot be empty or contain only whitespace.")
        raise ValidationError("Value cannot be empty or contain only whitespace.")
    return value



def validate_is_ULID(value:str):
    '''
        Used in models to check if the passed str value can be converted into a ULID.
        catches ULID errors and raises them as ValidationErrors.
    '''
    try:
        return ULID.parse(value=value)
    except TypeError as e:
        raise ValidationError(repr(e))
    except ValueError as e:
        raise ValidationError(repr(e))



ascii_safe_name_validator = RegexValidator(
    regex=r'^[A-Za-z0-9 ._-&]*$',
    message='Name may only contain ASCII letters, digits, spaces, dashes, dots, and underscores.',
    code='invalid_name'
)


def validate_not_negative(value):
    '''
    Used in models that save a Numberic field which must not be negative ignoring None values.
    '''
    try:
        if value is not None and value < 0:
            raise ValidationError("Value can not be negative")
        else:
            return value
    except (TypeError,ValueError) as e:
        raise ValidationError("Invalid type or value")