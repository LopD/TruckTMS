## django lib
from django.db import models
from django.db.models import CheckConstraint, Q, functions
from django.core.validators import RegexValidator

## core
from core.validators import validate_not_whitespace_only
from core.models import Audited

## 3rd party libs
from ulid import ULID
from ulid_django.models import ULIDField

## custom libs
from .validators import *

## core
from core.validators import validate_is_ULID


class Location(Audited):
    
    '''
        The primary key is a ULID
    '''
    # id = ULIDField(primary_key=True, default=ULID, editable=False)

    '''
        Latitude field saved as pythons native floating point representation.
    '''
    lat = models.FloatField(blank=True,null=True, validators=[validate_lat]) 
    
    '''
        Longitude field saved as pythons native floating point representation.
    '''
    lng = models.FloatField(blank=True,null=True, validators=[validate_lng]) 

    '''
        Address of the location inside the city.
    '''
    address = models.CharField(max_length=255,blank=True,null=True)

    '''
        What is the city and zip code of this location.
    '''
    city = models.CharField(max_length=255,blank=True,null=True)
    state = models.CharField(max_length=255,blank=True,null=True)

    class Meta:
        constraints = [
            CheckConstraint(
                check=(Q(lat__isnull=True, lng__isnull=True) | Q(lat__isnull=False, lng__isnull=False)),
                name="Location_lat_lng_both_or_none"
            ),
            CheckConstraint(
                check=(Q(lat__isnull=False, lng__isnull=False) | (Q(lat__lt=-90, lat__gt=90) & Q(lng__lt=-180, lng__gt=180))),
                name="Location_lat_lng_invalid_value"
            )
        ]
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Ensures model is valid and passes all validators
        super().save(*args, **kwargs)