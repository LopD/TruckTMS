## rest framework
from rest_framework.permissions import DjangoModelPermissions,BasePermission
from rest_framework import exceptions,permissions

## django 
from django.contrib.auth.models import Permission,Group

## core
from core.utilities.checks import get_token_user_groups

## dispatch
from .models import *


class CoreBasePermissions(DjangoModelPermissions):
    '''
    Slightly modified rest_framework.permissions.DjangoModelPermissions class.
    '''
    
    model = Company                         ## What model is this permission used for
    admin_full_control = True               ## Does the admin user have full control over the model
    authenticated_users_only = True         ## Can only authenticated (logged in) users view,add,edit or delete objects
    perms_map = {                           ## Which permissions are required for what action (NOTE: put [] for no permissions required)
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        if self.admin_full_control and request.user and  request.user.is_authenticated and request.user.is_staff:
            return True        
        return super().has_permission(request,view)


    
    