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

## crm
from crm.models import Company

## this app
# from .validators import *


'''
    Payment type choices require acronyms so I made some up.
'''
PAYMENT_TYPE_CHOICES = {
    '$MILE'  : '$ per mile',
    '%REVE'  : '% per revenue',
    '$WEEK'  : 'flat $ per week',
}

'''
    The drivers current status based on his location. 
'''
DRIVER_STATUS_CHOICES = {
    'ON ROAD'  : 'The driver is currently on the road',
    'STANDBY'  : 'The driver is currently in the yard or on standby',
}


# Create your models here.
class Dispatcher(UserProfile):

    '''
        One-To-One link to the users profile model that is defined in the core app
    '''
    # profile = models.OneToOneField(user, on_delete=models.CASCADE, primary_key=True, related_name='dispatcher')  


    # def __str__(self):
    #     return self



class Driver(UserProfile):

    '''
        One-To-One link to the users profile model that is defined in the core app
    '''
    # profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True, related_name='driver')  ##related_name='driver'

    '''
        The dispatcher of this driver. 
        The dispatcher must work for a company.
    '''
    assigned_dispatcher = models.ForeignKey(
        Dispatcher,
        on_delete=models.PROTECT,
        null=False,
        blank=False,       
        related_name='drivers'    # This allows Company.drivers.all() access
    )

    
    '''
        What type of payment the driver is receiving.
    '''
    payment_type = models.CharField(choices=PAYMENT_TYPE_CHOICES, max_length= 5,null=False,blank=False,default='$MILE')
    
    '''
        The amount the driver is being payed. Note that this depends based on their payment type.
    '''
    pay_rate = models.DecimalField(
        null=False,
        blank=False,
        max_digits=19,
        decimal_places=2,
        default=0.0
    ) 

    '''
        Does this driver have the neccessary certifications to drive hazmat freigths.
        more info: https://www.hazmatuniversity.com/news/when-is-a-hazmat-endorsement-required-on-a-cdl/
    '''
    is_hazmat_endorsed = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )

    '''
        Does this driver have the neccessary certifications to drive tankers.
        more info: https://www.hazmatuniversity.com/news/when-is-a-hazmat-endorsement-required-on-a-cdl/
    '''
    is_tanker_endorsed = models.BooleanField(
        null=False,
        blank=False,
        default=False
    )

    
    '''
        What the drivers current location status is.
    '''
    status = models.CharField(choices=DRIVER_STATUS_CHOICES, max_length= 7,null=False,blank=False,default='STANDBY')

    

    class Meta:
        constraints = [
            CheckConstraint(check=Q(status__in=list(DRIVER_STATUS_CHOICES.keys())), name='driver_status_choices_violation'),
            CheckConstraint(check=Q(payment_type__in=list(PAYMENT_TYPE_CHOICES.keys())), name='driver_payment_type_choices_violation'),
        ]
    
    def __str__(self):
        return f"Driver:{self.userprofile_ptr_id}-{self.userprofile_ptr.user.username}"
    


class Manager(UserProfile):
    
    def __str__(self):
        return f"Manager:{self.userprofile_ptr_id}-{self.userprofile_ptr.user.username}"
    