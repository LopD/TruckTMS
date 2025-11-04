## rest_framework
from rest_framework import generics

## django_filters
from django_filters import rest_framework as filters

## core
from core.filters import AuditedFilter
from core.utilities.utils import str_to_bool

## 
from .models import *




class DriverFilter(filters.FilterSet):
    
    
    class Meta:
        model = Driver
        fields = '__all__'


class DispatcherFilter(filters.FilterSet):
    
    class Meta:
        model = Dispatcher
        fields = '__all__'



class ManagerFilter(filters.FilterSet):
    
    class Meta:
        model = Manager
        fields = '__all__'