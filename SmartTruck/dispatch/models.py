## django lib
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import CheckConstraint, Q, functions
from django.db.models.functions import Length
from django.db.models.expressions import Value
from django.db import transaction
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


## equipment_management
from equipment_management.models import *

## this app
from .validators import *

'''
    The drivers current status based on his location. 
'''
LOAD_STATUS_CHOICES = { 
    'WAITING'    : 'The load is has yet to be delivered',
    'ON ROAD'    : 'The load is in the process of being delivered',
    'DELIVERED'  : 'The load has been delivered',
}


class Route(Audited):

    locations = models.ManyToManyField(Location, through="RouteStop")

    '''
        The distance in miles from the start and destination.
    '''
    distance_miles = models.FloatField(
        default=0.0,
        blank=False,
        null=False
    )

    '''
        The link of the route.
        NOTE It's unknown how long the link will be so TextField is used as it does not enforce a length. Use a CharField if it is known
    '''
    route_link = models.TextField(
        blank=True,
        null=True
    )


    '''
        Custom name for the route so it can be found later easier.
    '''
    custom_name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    def delete(self, using=None, keep_parents=False):
        with transaction.atomic():
            # find all locations for this route
            for loc in self.locations.all():
                # if this location only appears in this route → delete it
                if not RouteStop.objects.filter(location=loc).exclude(route=self).exists():
                    loc.delete()
        return super().delete(using, keep_parents)


class RouteStop(models.Model):
    """
    junction table: each row is one stop belonging to a specific route
    with a specific order
    """
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=False,null=False)

    class Meta:
        unique_together = ("route", "order")
        ordering = ["order"]  # important → preserves stop order

    def __str__(self):
        return f"{self.route.name} → {self.location.name} (#{self.order})"



class Load(Audited):
    
    '''
        The driver that is assigned this load.
    '''
    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,       
        default=None,             # Sets default value to NULL/None
        related_name='loads'      # This allows Driver.loads.all() access
    )
    
    """
    Which company made this load.
    """
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=False,
        blank=False,       
        related_name='loads'      
    )
    
    """
    Which company is contracted to do this load.
    """
    contracted_company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,       
        default=None,             
        related_name='contracted_loads' 
    )

    '''
        Truck that is assigned to this load.
    '''
    truck = models.ForeignKey(
        Truck,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,       
        default=None,             # Sets default value to NULL/None
        related_name='loads'      # This allows Truck.loads.all() access
    )

    '''
        Trailer that is assigned to this load.
    '''
    trailer = models.ForeignKey(
        Trailer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,       
        default=None,             # Sets default value to NULL/None
        related_name='loads'      # This allows Trailer.loads.all() access
    )

    '''
        TODO: Auto create route if it does not exist
    '''
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        null=False,
        blank=False,       
        default=None,             # Sets default value to NULL/None
        related_name='loads'      # This allows Route.loads.all() access
    )

    '''
        Are the goods hazardous.
    '''
    is_hazmat = models.BooleanField(
        default=False,
        null=False,
        blank=False
    )

    '''
        When was the load picked up.
    '''
    pickup_datetime = models.DateTimeField(
        null=True,
        blank=True
        ## default=datetime.now ## don't
    )

    '''
        When was the load delivered.
    '''
    delivery_datetime = models.DateTimeField(
        null=True,
        blank=True
        ## default=datetime.now ## don't
    )

    '''
        When it was assigned to a driver.
    '''
    assignment_datetime = models.DateTimeField(
        null=True,
        blank=True
        ## default=datetime.now ## don't
    )

    '''
        The revenue received of the load.
    '''
    revenue = models.DecimalField(
        null=False,
        blank=False,
        default=0.0,
        max_digits=19,
        decimal_places=2
    )

    '''
        The weigth of the load in lbs.
        Does not need to specified at first but should be if possible.
    '''
    weigth_lbs = models.IntegerField(
        null=False,
        blank=False,
        default=0
    )
    
    '''
        What the drivers current location status is.
    '''
    status = models.CharField(choices=LOAD_STATUS_CHOICES, max_length=9,null=False,blank=False,default='WAITING')

    '''
        Additional information by the dispatcher for the driver when picking up the load.
    '''
    pickup_comment = models.TextField(null=True,blank=True)

    '''
        Additional information by the dispatcher for the driver when delivering the load.
    '''
    delivery_comment = models.TextField(null=True,blank=True)

    '''
        Additional information by the dispatcher for the load. Can be anything.
    '''
    details = models.TextField(null=True,blank=True)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(status__in=list(LOAD_STATUS_CHOICES.keys())), name='load_status_choices_violation'),
        ]
    
    def save(self, *args, **kwargs):
        ## set assigned truck by default if not specified        
        # self.company    = self.driver.userprofile_ptr.company if self.driver is not None and self.company is None else None
        # self.truck      = self.driver.assigned_truck if self.driver is not None and self.truck is None else None
        # self.trailer    = self.driver.assigned_trailer if self.driver is not None and self.trailer is None else None
        self.full_clean() 
        super().save(*args, **kwargs)

