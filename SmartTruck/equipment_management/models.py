## django lib
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import CheckConstraint, Q, functions
from django.db.models.functions import Length
from django.db.models.expressions import Value
from django.core.exceptions import ValidationError

## 3rd party libs
from phonenumber_field.modelfields import PhoneNumberField
from ulid import ULID
from ulid_django.models import ULIDField

## core
from core.models import UserProfile, Audited
from core.validators import validate_not_whitespace_only, ascii_safe_name_validator, validate_not_negative

## geolocation
from geolocation.models import Location
from geolocation.validators import *

##  user_management
from user_management.models import *

## this app
from .validators import *

'''
    What types of trailers there are
'''
TRAILER_TYPE_CHOICES = {
    'VAN'     : 'The trailer is a van',
    'DRYVAN'  : 'The trailer is a dry van',
    'REFEER'  : 'The trailer is a refeer',
}

'''
    The trailers current status based on his location. 
'''
TRAILER_STATUS_CHOICES = {
    'ON ROAD'  : 'The trailer is currently on the road',
    'STANDBY'  : 'The trailer is currently in the yard or on standby',
}

'''
    The trucks current status based on his location. 
'''
TRUCK_STATUS_CHOICES = {
    'ON ROAD'  : 'The truck is currently on the road',
    'STANDBY'  : 'The truck is currently in the yard or on standby',
}

class Equipment(Audited):
    '''
        Is this equipment being leased.
    '''
    is_leased = models.BooleanField(
        default=False,
        blank=False,
        null=False
    )

    '''
        The lease rate.
    '''
    lease_rate = models.DecimalField(
        blank=False,
        null=False,
        default=0.0,
        max_digits=19,
        decimal_places=2
    )

    '''
        Is this piece of equipment still operational/in use.
    '''
    is_active = models.BooleanField(
        blank=False,
        null=False,
        default=True
    )

    @staticmethod
    def base_constraints(class_name: str):
        if class_name is None or class_name == "":
            raise Exception("class_name not specified. class_name must be unique in the database")
        return [
            
        ]

    class Meta:
        abstract = True



class TransportationEquipment(Equipment):
    
    '''
        Digits of the VIN.
    '''
    vin = models.CharField(
        max_length=17, 
        unique=True,
        blank=False,
        null=False,
        validators=[validate_not_whitespace_only, validate_vin]
    )

    '''
    '''
    license_plate_state_usps_abbreviation = models.CharField(
        max_length=2,
        null=True,
        blank=True,
        validators=[validate_usps_abbreviation]
    )

    '''
        License plate number is usually only 7 characters long but that depends on the state.
    '''
    license_plate_number = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )

    '''
        The weigth of the equipment in lbs.
        Does not need to specified at first but should be if possible.
    '''
    weigth_lbs = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=2,
        validators=[validate_not_negative]
    )

    '''
        The length of the equipment in feet (imperial units).
        Does not need to specified at first but should be if possible.
    '''
    length_ft = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=2,
        validators=[validate_not_negative]
    )

    @staticmethod
    def base_constraints(class_name: str):
        if class_name is None or class_name == "":
            raise Exception("class_name not specified. class_name must be unique in the database")
        return Equipment.base_constraints(class_name.lower()) + [ 
            CheckConstraint(check=~Q(vin=''), name=f"{class_name.lower()}_vin_not_empty" ),
            CheckConstraint(check=~(Q(weigth_lbs__isnull=False) & Q(weigth_lbs__lt=0)), name=f"{class_name}_weigth_lbs_is_negative" ),
            CheckConstraint(check=~(Q(length_ft__isnull=False) & Q(length_ft__lt=0)), name=f"{class_name}_length_ft_is_negative" ),
        ]

    def save(self, *args, **kwargs):
        self.vin = self.vin.strip().upper()
        self.license_plate_state_usps_abbreviation =  self.license_plate_state_usps_abbreviation.strip().upper() if self.license_plate_state_usps_abbreviation is not None else self.license_plate_state_usps_abbreviation
        self.license_plate_number = self.license_plate_number.strip() if self.license_plate_number is not None else self.license_plate_number
        super().save(*args, **kwargs)        


    class Meta:
        abstract = True




class Truck(TransportationEquipment):

    '''
        The company that this truck belongs to.
    '''
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,  
        null=False,
        blank=False,
        related_name='trucks',    # This allows Company.trucks.all() access
    )

    
    '''
        What the trucks current location status is.
    '''
    status = models.CharField(choices=TRUCK_STATUS_CHOICES, max_length= 7,null=False,blank=False,default='STANDBY')

    '''
        This field is only used for additional info. 
        The driver does not need to use the assigned truck/trailer for every load but in 99% cases he will.
    '''
    assigned_driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,       
        default=None,             # Sets default value to NULL/None
        related_name='assigned_truck'
    )
    

    class Meta:
        constraints = TransportationEquipment.base_constraints("Truck") + [
            CheckConstraint(check=Q(status__in=list(TRUCK_STATUS_CHOICES.keys())), name='truck_status_choices_violation'),
        ]
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Ensures model is valid
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Truck:{self.vin}-{self.company.name}-{self.assigned_driver.userprofile_ptr.user.username if self.assigned_driver is not None else ""}"



class Trailer(TransportationEquipment):

    '''
        The company this trailer belongs to.
    '''
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,  
        null=False,
        blank=False,
        related_name='trailers'    # This allows Company.trailers.all() access
    )

    
    '''
        What the trailers current location status is.
    '''
    status = models.CharField(choices=TRAILER_STATUS_CHOICES, max_length= 7,null=False,blank=False,default='STANDBY')

    
    '''
        What type is this trailer.
    '''
    type = models.CharField(choices=TRAILER_TYPE_CHOICES, max_length= 6,null=False,blank=False,default='VAN')

    '''
        This field is only used for additional info. 
        The driver does not need to use the assigned truck/trailer for every load but in 99% cases he will.
    '''
    assigned_driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,       
        default=None,             # Sets default value to NULL/None
        related_name='assigned_driver'
    )

    class Meta:
        constraints = TransportationEquipment.base_constraints("Trailer") +  [
            CheckConstraint(check=Q(status__in=list(TRAILER_STATUS_CHOICES.keys())), name='trailer_status_choices_violation'),
            CheckConstraint(check=Q(type__in=list(TRAILER_TYPE_CHOICES.keys())), name='trailer_type_choices_violation'),
        ]
    
    def save(self, *args, **kwargs):
        self.full_clean() ## ensures the data passes all validators
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Trailer:{self.vin}-{self.company.name}-{self.assigned_driver.userprofile_ptr.user.username if self.assigned_driver is not None else ""}"
