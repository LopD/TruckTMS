'''
    This is a custom authenticator class
    https://docs.djangoproject.com/en/5.2/topics/auth/customizing/
    AUTHENTICATION_BACKENDS are defined in "SmartTruck/settings.py"
'''

## django libs
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

class AuthBackend(BaseBackend): 
    
    def authenticate(self, request, username=None, password=None, email=None): ## token=None
        
        if password is None:
             return None
        
        ## get the AUTH_USER_MODEL that is used for this project 
        user_model = get_user_model()
        user = None
        if username is not None:
            user = user_model.objects.filter(username=username).first()
        if user is None and email is not None:
            user = user_model.objects.filter(email=email).first()
        
        ## Staff users should go through the default django authentication backend since they are the default django admin role
        # if user is not None and user.is_staff:
        #     return None
        
        return user
    
        # if not user.is_staff:
        #     return None
        #     
        # Check the username/password and return a user.
        # return None if no user can be found

        ## https://docs.djangoproject.com/en/5.2/ref/exceptions/#django.core.exceptions.PermissionDenied
        # if user is not authenticated_or_something:
            # raise PermissionDenied 

        