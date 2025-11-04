## rest framework
from rest_framework.permissions import DjangoModelPermissions,BasePermission
from rest_framework import exceptions,permissions

## django 
from django.contrib.auth.models import Permission,Group

## core
from core.utilities.checks import get_token_user_groups
from core.permissions import CoreBasePermissions

## dispatch
from dispatch.models import Dispatcher

## dispatch
from .models import *


class CompanyPermissions(CoreBasePermissions):
    '''
    Slightly modified rest_framework.permissions.DjangoModelPermissions class.
    '''
    
    model = Company                         ## What model is this permission used for
    
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
        
        ## 
        if 'Dispatchers' in  user_groups:
            return True
        return False



class CompanyIndustryPermissions(CoreBasePermissions):
    '''
    Slightly modified rest_framework.permissions.DjangoModelPermissions class.
    '''
    
    model = CompanyIndustry                 ## What model is this permission used for
    
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
        
        ## 
        if 'Dispatchers' in  user_groups:
            return True
        return False
        