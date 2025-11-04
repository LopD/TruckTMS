## rest_framework
from rest_framework import generics

## django_filters
from django_filters import rest_framework as filters

## core
from core.filters import AuditedFilter
from core.utilities.utils import str_to_bool

## 
from .models import *





class LoadFilter(AuditedFilter):
    
    pickup_datetime = filters.DateTimeFromToRangeFilter(field_name='pickup_datetime')
    delivery_datetime = filters.DateTimeFromToRangeFilter(field_name='delivery_datetime')
    assignment_datetime = filters.DateTimeFromToRangeFilter(field_name='assignment_datetime')
    dispatcher = filters.NumberFilter(field_name='driver__assigned_dispatcher', lookup_expr='exact')

    ##NOTE: simple filtering will not work for nested routes so the following will not work, you must go to the list() in the view class and handle those query params there
    # route_to_location_city_name = filters.CharFilter(field_name='route__from_location__city__name',lookup_expr='icontains')
    # route_from_location_city_name = ...
    
    class Meta:
        model = Load
        # fields = '__all__'
        exclude = ['pickup_comment','delivery_comment']


        

