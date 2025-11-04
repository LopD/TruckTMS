## rest framework
from rest_framework.permissions import DjangoModelPermissions,BasePermission
from rest_framework import exceptions,permissions

## django 
from django.contrib.auth.models import Permission,Group

## core
from core.utilities.checks import get_token_user_groups
from core.permissions import CoreBasePermissions

## dispatch
from .models import *


class LoadPermissions(CoreBasePermissions):
    '''
    Slightly modified rest_framework.permissions.DjangoModelPermissions class for the dispatch.models.Load model.
    '''
    
    model = Load                            ## What model is this permission used for


    ## only called when GET,POST,... method is called on a single object (E.g. loads/32)
    def has_object_permission(self, request, view, obj):
        return True
    
        if request.user and self.admin_full_control and request.user.is_staff:
            return True
        
        ## get user groups from token
        user_groups = get_token_user_groups(request)
        
        if 'Dispatchers' in  user_groups:            ## dispatcher can see all loads but edit only his own and unassigned loads
            
            ## Dispatchers can view all loads
            if request.method in permissions.SAFE_METHODS:
                return True
            
            ## Dispatchers can edit unassigned loads
            load_driver = getattr(obj, 'driver', None)
            if load_driver is None:
                return True
            
            ## Dispatchers can edit their loads
            load_dispatcher_id = getattr(load_driver, 'dispatcher_id', None)
            if load_dispatcher_id is not None and request.user.id == load_dispatcher_id:
                return True
            
        if 'Drivers' in user_groups:               ## drivers can only see their loads
            
            if request.method in permissions.SAFE_METHODS:
                load_driver_id = getattr(obj, 'driver_id', None)
                if load_driver_id is not None and request.user.id == load_driver_id:
                    return True

        ## default:        
        return False



class RoutePermissions(CoreBasePermissions):
    '''
    Slightly modified rest_framework.permissions.DjangoModelPermissions class for the dispatch.models.Route model.
    '''
    
    model = Route                           ## What model is this permission used for

    def has_object_permission(self, request, view, obj):
        return True
    
        if request.user and self.admin_full_control and request.user.is_staff:
            return True
        
        # is the request method any of the following: GET, HEAD or OPTIONS
        if request.method in permissions.SAFE_METHODS:
            ## anyone can view the object
            return True

        ## get user groups from token
        user_groups = get_token_user_groups(request)
        
        ## Dispatchers can edit his routes and any unassigned routes
        if 'Dispatchers' in  user_groups:  
            if obj.loads is None or len(obj.loads) <= 0:
                return True
            ## TODO: improve this
            ## combining 3 tables is BS but idk how to improve it
            return self.model.objects.filter(pk=obj.pk,loads__driver__dispatcher_id=request.user.id).count() > 0
            
            
        ## default:        
        return False
    





