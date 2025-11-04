## django lib
from django.core.exceptions import ValidationError

def validate_vin(value):
    '''
    Validates that the string is a valid VIN number.
    '''
    if not isinstance(value,str):
        print('VIN is not a string.')
        raise ValidationError('VIN is not a string.')
    # if not (value.isalnum() and value.isupper()):
    #     raise ValidationError('VIN abbreviation must consist of only uppercase letters or digits.')
    return value