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

from user_management.models import Driver

## core
from core.models import UserProfile

## geolocation
from geolocation.models import Location
from geolocation.serializers import LocationSerializer

## ulid
from ulid import ULID


class RegisterDriverSerializer(serializers.ModelSerializer):
    '''
    Registers a new driver.
    '''

    class Meta:
        model = Driver
        fields = '__all__'


    def validate_profile(self, value):
        query = Driver.objects.filter(profile=value) 
        if query.exists():
            raise serializers.ValidationError("Profile already has a Driver associated with it.")
        return value


    def create(self, validated_data):
        ## create driver
        driver = Driver.objects.create(
            profile=validated_data['profile'],
            phone_number=validated_data['phone_number'],
        )
        return driver






class TruckSerializer(serializers.ModelSerializer):

    class Meta:
        model = Truck
        # exclude = ['company']
        fields = '__all__'

    def create(self, validated_data):
        raise serializers.ValidationError("Serializer can not create objects!")
        



class TrailerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trailer
        exclude = ['company']
        # fields = '__all__'

    def create(self, validated_data):
        raise serializers.ValidationError("Serializer can not create objects!")




class TruckCreationSerializer(serializers.ModelSerializer):

    company = serializers.PrimaryKeyRelatedField(many=False, required=False, queryset=Company.objects.all())

    def validate(self, data):
        
        ## If no company was specified then put the current users dispatcher company if it exists.
        request = self.context.get('request', None)
        if data.get('company',None) is not None or request is None:
            return super().validate(data)  
        
        user_id = request.auth.get('user_id',None)
        
        company_id = UserProfile.objects.filter(pk=user_id).values_list('company_id', flat=True).first()
        if company_id is not None:
            ## NOTE:This creates an unsaved model instance with only the id set. 
            ## NOTE: Django will not query the database for this. It just uses the given primary key when saving. 
            ## NOTE: This means that a model with that ID must already exist in the database or you'll get a Database error
            data['company'] = Company(id=company_id)
    
        return super().validate(data)

    def create(self, validated_data):
        ## this try catch block returns any Django validation errors into rest_framework serializer validation erors
        try:
            return self.Meta.model.objects.create(**validated_data)
        except DjangoValidationError as e:
            raise DRFValidationError(e.message_dict)
        
    class Meta:
        model = Truck
        fields = '__all__'
    


class TrailerCreationSerializer(serializers.ModelSerializer):

    company = serializers.PrimaryKeyRelatedField(many=False, required=False, queryset=Company.objects.all())

    def validate(self, data):
        
        ## If no company was specified then put the current users dispatcher company if it exists.
        request = self.context.get('request', None)
        if data.get('company',None) is not None or request is None:
            return super().validate(data)  
        
        user_id = request.auth.get('user_id',None)
        
        company_id = UserProfile.objects.filter(pk=user_id).values_list('company_id', flat=True).first()
        if company_id is not None:
            ## NOTE:This creates an unsaved model instance with only the id set. 
            ## NOTE: Django will not query the database for this. It just uses the given primary key when saving. 
            ## NOTE: This means that a model with that ID must already exist in the database or you'll get a Database error
            data['company'] = Company(id=company_id)
    
        return super().validate(data)


    def create(self, validated_data):
        ## this try catch block returns any Django validation errors into rest_framework serializer validation erors
        try:
            return self.Meta.model.objects.create(**validated_data)
        except DjangoValidationError as e:
            raise DRFValidationError(e.message_dict)

    class Meta:
        model = Trailer
        fields = '__all__'
        

