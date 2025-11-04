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
from rest_framework.permissions import IsAuthenticated
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
from .paginations import *
from .permissions import *
from .filters import *

# Create your views here.



class LoadViewSet(viewsets.ModelViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    queryset = Load.objects.all()
    serializer_class = LoadSerializer
    permission_classes = [LoadPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter] ## SearchFilter
    filterset_class = LoadFilter
    search_fields = [] ## 'route__from_location__city_name',
    ordering_fields = ['id','is_hazmat','pickup_datetime','delivery_datetime','assignment_datetime','revenue','weigth_lbs','status','driver','truck','trailer'] 
    ordering = ['-pk']     ## default filtering field (NOTE: this field must exist in the queryset model so 'company_name' will not work)

    def get_queryset(self):
        
        ## Return all loads if no user is specified
        user_id = self.request.user.id
        if user_id is None or self.request.user.is_staff:
            return self.queryset
        
        ## Return all loads based on the user role/group
        from core.utilities.checks import get_token_user_groups
        user_groups = get_token_user_groups(self.request)
        company_id = UserProfile.objects.filter(pk=user_id).values_list('company_id', flat=True).first()

        if 'Managers' in  user_groups:            
            return self.queryset.filter( Q(company_id=company_id) )
        elif 'Dispatchers' in  user_groups:            
            return self.queryset.filter( Q(company_id=company_id) & (Q(driver__assigned_dispatcher_id=user_id) | Q(driver_id=None)) )
        elif 'Drivers' in user_groups:               
            return self.queryset.filter(driver_id=user_id)
        else:
            return self.queryset

    def get_serializer_class(self):
        if self.request.method in ["POST",'PUT','PATCH']:
            return LoadCreationSerializer
        return self.serializer_class

    def list(self, request,*args, **kwargs):
        
        ## complex user queries for route from and to locations
        # route_to_location_city_name = self.request.query_params.get('route_to_location_city_name',None)
        # if route_to_location_city_name is not None:
        #     self.queryset = self.get_queryset().filter(route__to_location__city__name__icontains=route_to_location_city_name)
        # route_from_location_city_name = self.request.query_params.get('route__from_location__city__name',None) 
        # if route_from_location_city_name is not None:
        #     self.queryset = self.get_queryset().filter(route__from_location__city__name__icontains=route_from_location_city_name)
        
        ## default return
        return super().list(request, *args, **kwargs)
        
    
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk):
    #     pass





class RouteViewSet(viewsets.ModelViewSet):
    
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [RoutePermissions] 
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter] ## SearchFilter
    # filterset_class = LoadFilter
    search_fields = [] ## 'route__from_location__city_name',
    ordering_fields = ['pk'] 
    ordering = ['-pk']     


    def get_queryset(self):
        
        ## Return all if no user is specified
        user_id = self.request.user.id
        if user_id is None or self.request.user.is_staff:
            return self.queryset
        
        ## Return all loads based on the user role/group
        from core.utilities.checks import get_token_user_groups
        user_groups = get_token_user_groups(self.request)
        company_id = UserProfile.objects.filter(pk=user_id).values_list('company_id', flat=True).first()

        if 'Managers' in  user_groups:
            return self.queryset.filter( Q(company_id=company_id) )
        elif 'Dispatchers' in  user_groups:
            return self.queryset.filter( Q(company_id=company_id) )
            # return self.queryset.annotate(incoming_count=Count('from_routes')).filter(incoming_count=0)
        elif 'Drivers' in user_groups:
            return self.queryset.filter( Q(company_id=company_id) )
            # routes = self.queryset.filter(from_routes__len=user_id).distinct()
            return routes 
        else:   
            return self.queryset

    def get_serializer_class(self):
        if self.request.method in ["POST"]:
            return RouteCreationSerializer
        return self.serializer_class









