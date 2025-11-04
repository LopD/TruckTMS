## rest_framework
from rest_framework import generics

## django_filters
from django_filters import rest_framework as filters

## crm
from .models import *


## Filters documentation
## https://django-filter.readthedocs.io/en/latest/guide/rest_framework.html#
## https://www.django-rest-framework.org/api-guide/filtering/
class AuditedFilter(filters.FilterSet):
    created_at = filters.DateTimeFromToRangeFilter(field_name='created_at')
    updated_at = filters.DateTimeFromToRangeFilter(field_name='updated_at')

    class Meta:
        model = Audited
        fields = ['created_at','updated_at']
        # exclude = ['created_at','updated_at']
        