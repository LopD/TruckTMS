## django lib
from django.db import models
# from django.contrib.auth import get_user_model
from django.db.models import CheckConstraint, Q, functions
from django.core.exceptions import ValidationError

## 3rd party libs
from phonenumber_field.modelfields import PhoneNumberField
from ulid import ULID
from ulid_django.models import ULIDField

## core
# from core.models import Audited
from core.validators import validate_not_whitespace_only 

## geolocation
# from geolocation.models import Location



class CompanyIndustry(models.Model):
    
    '''
        Name of the company industry.
    '''
    name = models.CharField(
        max_length=80, 
        blank=False, 
        null=False, 
        unique=True,
        validators=[validate_not_whitespace_only]
    )

    class Meta:
        constraints = [
            CheckConstraint(check=~Q(name=''), name='companyindustry_name_not_empty'),
        ]

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        self.full_clean()  # Ensures model is valid
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}"


class Company(models.Model):
    
    '''
        Name of the company.
    '''
    name = models.CharField(
        max_length=80, 
        blank=False, 
        null=False, 
        unique=True,
        validators=[validate_not_whitespace_only]
    )
    '''
        The company phone number. 
        If you are using a CharField then when storing prefix and suffix: len=5+15+11=31 in the worst case scenario.
    '''
    phone_number = PhoneNumberField(region='US', null=True, blank=True)  # adjust region if needed

    '''
        The company email. 
        https://docs.djangoproject.com/en/5.2/ref/models/fields/#emailfield
    '''
    email = models.EmailField(null=True,blank=True) 

    '''
        The DOT number of the company. Just the digits.
        https://www.tafs.com/dot-number-mc-number-differences/
    '''
    dot_number = models.CharField(max_length=7,null=True,blank=True)

    '''
        The MC number of the company.
        https://www.tafs.com/dot-number-mc-number-differences/
        https://www.operatingauthority.com/fmcsa-abruptly-shifts-to-seven-digit-mc-numbers/
    '''
    mc_number = models.CharField(max_length=7, null=True,blank=True)
    ## For instance, a truck operating out of California would have a dot number: USDOT1523020 printed on the door of the cab, and below it would have the MC number: CA 309886. This would indicate that the company is registered with the Department of Transportation and is a valid Motor carrier in the state of California.
    
    '''
        This is the website url of the company.
    '''
    website = models.URLField(max_length=128, null=True,blank=True)

    '''
        What industries does this company belong to.
    '''
    industries = models.ManyToManyField(
        CompanyIndustry, 
        related_name="companies"
    )

    class Meta:
        constraints = [
            CheckConstraint(check=~Q(name=''), name='company_name_not_empty'),
        ]

    def save(self, *args, **kwargs):
        self.name = self.name.strip() if self.name is not None else self.name
        self.dot_number = self.dot_number.strip() if self.dot_number is not None else self.dot_number
        self.mc_number = self.mc_number.strip() if self.mc_number is not None else self.mc_number
        self.full_clean()  # Ensures model is valid
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}-{self.dot_number}-{self.mc_number}"








