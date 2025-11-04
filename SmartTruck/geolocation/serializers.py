## rest framework
from rest_framework import serializers

## django lib
from django.db import models
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth import get_user_model

## custom django extensions
from ulid_django.converters import ULIDConverter

## custom models
from .models import *
from core.models import UserProfile

## utilities
from .utilities.geocoding import Geocoder





class LocationSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Location
        # exclude = ['created_at','updated_at','city']
        fields = '__all__'

    def validate(self, data):
        # if (data.get('lat',None) is None or data.get('lng',None) is None) and data.get('address',None) is None and data.get('id',None) is None:
        #     raise serializers.ValidationError({"location":["No address/coordinates/id specified"]})
        return super().validate(data)


    def create(self,validated_data):
        
        obj_lat = validated_data.get('lat',None)
        obj_lng = validated_data.get('lng',None)

        geocoder = Geocoder(provider="osm") 

        ## geolocation data for specified location
        new_lat,new_lng, display_name, address, city_name, state_name = None, None, None, None, None, None
        
        
        if obj_lat is not None and obj_lng is not None:
            try:
                location = Location.objects.get(lat=obj_lat,lng=obj_lng)
                if location is not None:
                    return location
            except Location.DoesNotExist:
                pass
            except MultipleObjectsReturned as e:
                raise serializers.ValidationError(repr(e))
            
            new_lat,new_lng, display_name, address, city_name, state_name = geocoder.reverse_geocode(lat=obj_lat,lon=obj_lng)

        else: ## obj_address is not None:
            try:
                location = Location.objects.get(address=validated_data.get('address',None))
                if location is not None:
                    return location
            except Location.DoesNotExist:
                pass
            except MultipleObjectsReturned as e:
                raise serializers.ValidationError(repr(e))
            
            new_lat,new_lng, display_name, address, city_name, state_name = geocoder.geocode(address=validated_data.get('address',None))    

        ## hot swap coordinates if they were not found (this should never happen, if it does then this would be the problem of Geocoder class)
        if new_lat is None or new_lng is None:
            new_lat, new_lng = obj_lat, obj_lng
        
        
        new_obj, is_created = Location.objects.get_or_create( ## exceptions: ## MultipleObjectsReturned
            lat=new_lat,
            lng=new_lng,
            city=city_name,
            state=state_name,
            defaults={'address':address}
        )
        return new_obj

   