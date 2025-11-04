## django libs
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate   
from django.shortcuts import render
from django.db.models import Q
from django.db import transaction, IntegrityError
from django.db.models import Count
from django.core.exceptions import ValidationError as DjangoValidationError 

## rest framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes,action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework import permissions
from rest_framework.serializers import ValidationError as DRFValidationError
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser

## django_filters
from django_filters.rest_framework import DjangoFilterBackend

## core
from core.utilities.checks import request_auth_has_group, get_token_userid, get_request_file
from core.utilities.utils import str_to_bool

## dispatch
from .models import *
from .serializers import *
from .permissions import *
from .filters import *

# Create your views here.


# Create your views here.
class DriverViewSet(viewsets.ModelViewSet):
    
    queryset = Driver.objects.all().order_by('pk')
    serializer_class = DriverSerializer
    permission_classes = [DriverPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter] ## SearchFilter
    filterset_class = DriverFilter
    search_fields = ['userprofile_ptr__user__first_name'] ## user_profile__user__first_name
    ordering_fields = ['pk','userprofile_ptr__user__first_name','userprofile_ptr__company_id'] 
    ordering = ['pk']


    def get_queryset(self):

        ## Return all if no user is specified
        user_id = self.request.user.id
        if user_id is None:
            return self.queryset
        
        ## Return all loads based on the user role/group
        from core.utilities.checks import get_token_user_groups
        user_groups = get_token_user_groups(self.request)
        
        if 'Managers' in  user_groups:            
            return self.queryset
        if 'Dispatchers' in  user_groups:            ## dispatcher can see his loads and unassigned loads
            return self.queryset.filter(assigned_dispatcher_id=user_id)
        elif 'Drivers' in user_groups:               ## drivers can only see their loads
            return self.queryset.filter(pk=user_id)
        else:
            return self.queryset

    def get_serializer_class(self):
        if self.request.method in ["POST"]: ## SAFE_METHODS
            return DriverCreationSerializer
        if self.request.method in ["PUT","PATCH"]: ## SAFE_METHODS
            return DriverUpdateSerializer
        return self.serializer_class
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)



# Create your views here.
class DispatcherViewSet(viewsets.ModelViewSet):
    
    queryset = Dispatcher.objects.all().order_by('pk')
    serializer_class = DispatcherSerializer
    permission_classes = [DispatcherPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter] ## SearchFilter
    filterset_class = DispatcherFilter
    search_fields = ['userprofile_ptr__user__first_name'] ## user_profile__user__first_name
    ordering_fields = ['pk','userprofile_ptr__user__first_name','userprofile_ptr__company_id'] 
    ordering = ['pk']


    def get_queryset(self):

        ## Return all if no user is specified
        user_id = self.request.user.id
        if user_id is None:
            return self.queryset
        
        ## Return all loads based on the user role/group
        from core.utilities.checks import get_token_user_groups
        user_groups = get_token_user_groups(self.request)
        
        if 'Managers' in  user_groups:            
            return self.queryset
        if 'Dispatchers' in  user_groups:           
            return self.queryset.filter(pk=user_id)
        else:
            return self.queryset

    def get_serializer_class(self):
        if self.request.method in ["POST"]: ## SAFE_METHODS
            return DispatcherCreationSerializer
        if self.request.method in ["PUT","PATCH"]: ## SAFE_METHODS
            return DispatcherUpdateSerializer
        return self.serializer_class
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
        

class DispatcherViewSet(viewsets.ModelViewSet):
    
    queryset = Manager.objects.all().order_by('pk')
    serializer_class = ManagerSerializer
    permission_classes = [ManagerPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter] ## SearchFilter
    filterset_class = ManagerFilter
    search_fields = ['userprofile_ptr__user__first_name'] ## user_profile__user__first_name
    ordering_fields = ['pk','userprofile_ptr__user__first_name','userprofile_ptr__company_id'] 
    ordering = ['pk']


    def get_queryset(self):
        return self.queryset

    def get_serializer_class(self):
        if self.request.method in ["POST"]: ## SAFE_METHODS
            return ManagerCreationSerializer
        if self.request.method in ["PUT","PATCH"]: ## SAFE_METHODS
            return ManagerUpdateSerializer
        return self.serializer_class
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
        

