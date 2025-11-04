## rest framework
from rest_framework.permissions import DjangoModelPermissions,BasePermission
from rest_framework import exceptions,permissions

## django 
from django.contrib.auth.models import Permission,Group

## core
from core.utilities.checks import get_token_user_groups

## dispatch
from .models import *

class WebsocketBasePermission():
    """
    Abstract custom permission class for authenticating accepting websocket connections.
    """
    admin_full_control = True               ## Does the admin user have full control over the model
    authenticated_users_only = False        ## Can only authenticated (logged in) users view,add,edit or delete objects
    allowed_user_groups = []                ## Which user groups are allowed access

    def has_permission(self, scope: dict) -> bool:
        pass

    # def __call__(self, *args, **kwds):
    #     pass
        


class VehicleTrackingPermission(WebsocketBasePermission): 
    """
    Global permission check for blocked IPs.
    """
    admin_full_control = True               ## Does the admin user have full control over the model
    authenticated_users_only = True         ## Can only authenticated (logged in) users view,add,edit or delete objects
    allowed_user_groups = ['Dispatchers']   ## Which user groups are allowed access

    def has_permission(self, scope: dict) -> bool:
        """
        Assumes scope is a dict that has a valid "user" and "groups" field. Where "user" is a valid "get_user_model()" object.
        """
        if not self.authenticated_users_only:
            return True
        
        if scope is None:
            return False
        
        user = scope.get("user",None)
        if user is None:
            return False

        if self.admin_full_control and user.is_superuser:
            return True

        if len(self.allowed_user_groups) > 0:    
            user_groups = scope.get("groups",[])
            if not any(user_group in self.allowed_user_groups for user_group in user_groups):                
                return False
        
        return True
    