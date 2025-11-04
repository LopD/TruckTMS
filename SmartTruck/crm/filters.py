## rest_framework
from rest_framework import generics

## django_filters
from django_filters import rest_framework as filters

## core
from core.filters import AuditedFilter

## user_management
from user_management.models import Dispatcher

## 
from .models import *




class CompanyFilter(filters.FilterSet):
    
    is_blacklisted = filters.BooleanFilter(method='filter_is_blacklisted')
    exclude_self = filters.BooleanFilter(method='filter_exclude_self')
    
    def filter_is_blacklisted(self, qs, name, value):
        from crm.models import Blacklist    
            
        current_dispatcher = Dispatcher.objects.get(pk=self.request.user.id)
        if current_dispatcher is not None:
            blacklisted_companies_ids = Blacklist.objects.filter(company_id=current_dispatcher.company_id).values_list('blacklisted_company',flat=True)
            if value:
                return qs.filter(pk__in=blacklisted_companies_ids)
            else:
                return qs.exclude(pk__in=blacklisted_companies_ids)
        
        return qs
    
    
    def filter_exclude_self(self, qs, name, value):
        if not value:
            return qs

        current_dispatcher = Dispatcher.objects.get(pk=self.request.user.id)
        if current_dispatcher is not None:
            if value:
                return qs.exclude(pk=current_dispatcher.company_id)
        
        return qs

    class Meta:
        model = Company
        fields = '__all__'


class CompanyIndustryFilter(filters.FilterSet):
    
    class Meta:
        model = CompanyIndustry
        fields = '__all__'
