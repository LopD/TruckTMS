## rest_framework
from rest_framework import generics

## django_filters
from django_filters import rest_framework as filters

## core
from core.filters import AuditedFilter
from core.utilities.utils import str_to_bool

## 
from .models import *


class EquipmentFilter(AuditedFilter):
    
    ## had overwrite them all
    length_ft = filters.RangeFilter(field_name='length_ft')
    lease_rate = filters.RangeFilter(field_name='lease_rate')
    weigth_lbs = filters.RangeFilter(field_name='weigth_lbs')
    is_leased = filters.BooleanFilter(field_name='is_leased')
    is_active = filters.BooleanFilter(field_name='is_active')


    class Meta:
        model = Equipment
        # exclude = ['created_at','updated_at']
        # exclude = ['is_active'] ## ,'length_ft','weigth_lbs','is_active','lease_rate','is_leased'
        fields = ['length_ft','weigth_lbs','lease_rate','is_leased','is_active'] ## 



class TransportationEquipmentFilter(EquipmentFilter):
    
    ## had overwrite them all
    vin = filters.CharFilter(field_name='vin', lookup_expr='icontains')
    license_plate_state_usps_abbreviation = filters.CharFilter(field_name='license_plate_state_usps_abbreviation', lookup_expr='exact')
    license_plate_number = filters.CharFilter(field_name='license_plate_number', lookup_expr='icontains')

    class Meta:
        model = TransportationEquipment
        fields = ['vin','license_plate_state_usps_abbreviation','license_plate_number']
        



class TrailerFilter(TransportationEquipmentFilter):
    
    class Meta:
        model = Trailer
        fields = '__all__'



class TruckFilter(TransportationEquipmentFilter):
    
    class Meta:
        model = Truck
        fields = '__all__'
