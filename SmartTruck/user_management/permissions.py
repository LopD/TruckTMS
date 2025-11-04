## rest framework
from rest_framework.permissions import DjangoModelPermissions,BasePermission
from rest_framework import exceptions,permissions

## django 
from django.contrib.auth.models import Permission,Group

## core
from core.utilities.checks import get_token_user_groups
from core.permissions import CoreBasePermissions

## 
from .models import *


class DriverPermissions(CoreBasePermissions):
    '''
    Slightly modified rest_framework.permissions.DjangoModelPermissions class for the dispatch.models.Driver model.
    '''
    
    model = Driver                          ## What model is this permission used for


    def has_object_permission(self, request, view, obj):
        return True
        if request.user and self.admin_full_control and request.user.is_staff:
            return True
        
        # is the request method any of the following: GET, HEAD or OPTIONS
        if request.method in permissions.SAFE_METHODS:
            ## anyone can view the object
            return True

        ## the dispatcher can edit,update,delete the driver
        driver_dispatcher_id = getattr(obj, 'dispatcher', None)
        if driver_dispatcher_id is not None and request.user.id == driver_dispatcher_id:
            return True
        
        return False



class DispatcherPermissions(CoreBasePermissions):
    '''
    Slightly modified rest_framework.permissions.DjangoModelPermissions class for the dispatch.models.Driver model.
    '''
    
    model = Dispatcher                          ## What model is this permission used for


    def has_object_permission(self, request, view, obj):
        return True
        if request.user and self.admin_full_control and request.user.is_staff:
            return True
        
        # is the request method any of the following: GET, HEAD or OPTIONS
        if request.method in permissions.SAFE_METHODS:
            ## anyone can view the object
            return True

        ## the dispatcher can edit,update,delete the driver
        driver_dispatcher_id = getattr(obj, 'dispatcher', None)
        if driver_dispatcher_id is not None and request.user.id == driver_dispatcher_id:
            return True
        
        return False



class ManagerPermissions(CoreBasePermissions):
    '''
    Slightly modified rest_framework.permissions.DjangoModelPermissions class for the dispatch.models.Driver model.
    '''
    
    model = Manager                          ## What model is this permission used for


    def has_object_permission(self, request, view, obj):
        return True
        if request.user and self.admin_full_control and request.user.is_staff:
            return True
        
        # is the request method any of the following: GET, HEAD or OPTIONS
        if request.method in permissions.SAFE_METHODS:
            ## anyone can view the object
            return True

        ## the dispatcher can edit,update,delete the driver
        driver_dispatcher_id = getattr(obj, 'dispatcher', None)
        if driver_dispatcher_id is not None and request.user.id == driver_dispatcher_id:
            return True
        
        return False

