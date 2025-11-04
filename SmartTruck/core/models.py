## django lib
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

## 3rd party libs
from phonenumber_field.modelfields import PhoneNumberField

## 
from crm.models import Company


# Create your models here.

'''
    Models that need timestamps of when they were created or updated should inherit this class.
    If you are curious as to why then read this article: https://www.b-list.org/weblog/2023/dec/12/django-model-inheritance/
'''
class Audited(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        abstract = True

''' 
    Extends the User model using a One-To-One Link
    This is where all the custom user data will be located (E.g their title)
'''
class UserProfile(models.Model):

    '''
        One-To-One link to the user model that is used by the Authentication backend
    '''
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True,related_name='userprofile') 

    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE, 
        null=False,
        blank=False,
        related_name='employees'
    )

    '''
        Did the user verify his email. Users that have not verified their email can not access the site.
    '''
    is_email_verified = models.BooleanField(default=False,null=False)

    '''
        The users phone number. 
        The driver and dispatcher will need phone numbers.
        If you are using a CharField then when storing prefix and suffix: len=5+15+11=31 in the worst case scenario.
    '''
    phone_number = PhoneNumberField(region='US',null=True,blank=True)  # adjust region if needed
    
    '''
    '''
    seniority = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    '''
        Additional information.
    '''
    description = models.TextField(null=True,blank=True)

