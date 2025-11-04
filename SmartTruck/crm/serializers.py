## rest framework
from rest_framework import serializers
from rest_framework.serializers import ValidationError as DRFValidationError

## django lib
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError 
from django.db import transaction

## django extensions
from ulid_django.converters import ULIDConverter

## custom models
from .models import *

## core
from core.models import UserProfile

## geolocation
from geolocation.models import Location
from geolocation.serializers import LocationSerializer

## 3rd pary libs
from phonenumber_field.serializerfields import PhoneNumberField

## ulid
from ulid import ULID


class CompanyIndustrySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CompanyIndustry
        fields = '__all__'    


class CompanyCreationSerializer(serializers.ModelSerializer):
    industries = serializers.PrimaryKeyRelatedField(many=True, required=False, queryset=CompanyIndustry.objects.all())

    class Meta:
        model = Company
        fields = '__all__'
        # exclude = ['industries'] ## overwritting industries


class CompanySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Company
        # exclude = ['industries'] 
        fields = '__all__'




    
    
