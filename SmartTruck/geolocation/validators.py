## django lib
from django.core.exceptions import ValidationError


def validate_lat(value):
    try:
        if value < -90 or value > 90:
            raise ValidationError("invalid value")
        else:
            return value
    except TypeError as te:
        raise ValidationError("invalid type")

def validate_lng(value):
    try:
        if value < -180 or value > 180:
            raise ValidationError("invalid value")
        else:
            return value
    except TypeError as te:
        raise ValidationError("invalid type")

def validate_zipcode(value):
    '''
        Validates that the input is a string of 5 digits.
    '''
    if not value.isdigit():
        raise ValidationError('Zip code must contain only digits.')
    
    if len(value) != 5:
        raise ValidationError('Zip code must be exactly 5 characters long.')
    
    return value

def validate_usps_abbreviation(value):
    '''
    Validates that the input is 2 characters long.
    '''
    if not isinstance(value,str):
        raise ValidationError('USPS abbreviation is not a string.')
    if len(value) != 2:
        raise ValidationError('USPS abbreviation must be exactly 2 characters long.')
    # if not value.isupper():
    #     raise ValidationError('USPS abbreviation must consist of only uppercase letters.')
    
    return value.upper()

