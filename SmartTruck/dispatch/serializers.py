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

## ulid
from ulid import ULID


class RouteStopSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = RouteStop
        fields = '__all__'
    
    def create(self, validated_data):
        raise DRFValidationError("can not create objects")



class RouteStopCreationSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = RouteStop
        fields = ['location','order']




class RouteSerializer(serializers.ModelSerializer):

    # locations = LocationSerializer(many=True)
    stops = RouteStopSerializer(source='routestop_set', many=True, read_only=True)

    class Meta:
        model = Route
        fields = '__all__'
    
    def create(self, validated_data):
        raise DRFValidationError("can not create objects")
    


class RouteCreationSerializer(serializers.ModelSerializer):

    stops = RouteStopCreationSerializer(many=True, write_only=True) 

    class Meta:
        model = Route
        fields = '__all__'

    def create(self, validated_data):
        stops_data = validated_data.pop('stops')
        request = self.context.get('request',None)

        with transaction.atomic():
            route = Route.objects.create(**validated_data)

            # iter through each stop
            for stop in stops_data:
                loc_data = stop.pop('location')

                location = Location.objects.create(**loc_data)
                # or get_or_create if you need location re-use

                RouteStop.objects.create(
                    route=route,
                    location=location,
                    **stop
                )
            return route



class LoadSerializer(serializers.ModelSerializer):
    
    route = RouteSerializer()
    
    class Meta:
        model = Load
        fields = '__all__'
    
    def create(self, validated_data):
        raise DRFValidationError("serializer can not create objects")


class LoadCreationSerializer(serializers.ModelSerializer):
    
    route = RouteCreationSerializer()
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(),required=False)
    
    class Meta:
        model = Load
        # exclude = ['id','route']
        fields = '__all__'

    
    def validate_driver(self, value):
        ## get request, user_id and user_groups
        request = self.context.get('request',None)
        user_id = None 
        user_groups = []
        if request is not None:
            user_id = request.user.id
            from core.utilities.checks import get_token_user_groups
            user_groups = get_token_user_groups(request)
        if user_id is None:
            return value
        company_id = UserProfile.objects.filter(pk=user_id).values_list('company_id', flat=True).first()

        ## check if the request user works for the same company as the dispatcher
        if ('Managers' in  user_groups or 'Dispatchers' in  user_groups) and value.company_id != company_id:
            raise DRFValidationError("Driver is not in your company")
        elif 'Dispatchers' in  user_groups:
            if value.assigned_dispatcher_id != user_id:
                raise DRFValidationError("Driver is not assigned to this dispatcher")
        return value


    def validate_company_create(self, value):
        ## get request, user_id and user_groups
        request = self.context.get('request',None)
        user_id = None 
        if request is not None:
            ## admins have full control
            if request.user is not None and request.user.is_staff and value is not None:
                return value
            user_id = request.user.id
        if user_id is None and value is not None: ## fuck it
            return value
        
        ## just return the company
        return UserProfile.objects.filter(pk=user_id).first().company
    
    
    def validate_contracted_company_create(self, value):
        """
        Returns the current users company.
        """
        if value is None:
            return None
        
        ## get request, user_id and user_groups
        request = self.context.get('request',None)
        user_id = None 
        if request is not None:
            ## admins have full control
            if request.user is not None and request.user.is_staff:
                return value
            user_id = request.user.id
        if user_id is None: ## fuck it
            return value
        
        users_company = UserProfile.objects.filter(pk=user_id).first().company
        if value != users_company:
            raise DRFValidationError( {"contracted_company": ["Can not contract company that is not yours"]})
        return value
    
    
    def validate_truck(self, value):
        ## get request, user_id and user_groups
        request = self.context.get('request',None)
        user_id = None 
        if request is not None:
            if request.user is not None and request.user.is_staff:
                return value
            user_id = request.user.id
        if user_id is None:
            return value
        company_id = UserProfile.objects.filter(pk=user_id).values_list('company_id', flat=True).first()
        
        ## check if the truck belongs to this users company
        if value.company_id != company_id:
            raise DRFValidationError("Truck is not part of your company")
        return value
    
    
    def validate_trailer(self, value):
        ## get request, user_id and user_groups
        request = self.context.get('request',None)
        user_id = None 
        if request is not None:
            if request.user is not None and request.user.is_staff:
                return value
            user_id = request.user.id
        if user_id is None:
            return value
        company_id = UserProfile.objects.filter(pk=user_id).values_list('company_id', flat=True).first()
        
        ## check if the truck belongs to this users company
        if value.company_id != company_id:
            raise DRFValidationError("Trailer is not part of your company")
        return value

    
    def validate(self, attrs):
        company = attrs.get('comapny',None)
        contracted_company = attrs.get('contracted_company',None)
        driver  = attrs.get('driver',None)
        truck  = attrs.get('truck',None)
        trailer  = attrs.get('trailer',None)
        
        ## check if driver is part of contracted_company
        if contracted_company is None and driver is not None:
            raise DRFValidationError({"driver":["Can not assign driver to load without contracted_company field"]})
        elif driver is not None and contracted_company is not None and driver.company != contracted_company:
            raise DRFValidationError({"driver":["is not part of contracted_company"]})
        
        ## check if truck is part of contracted_company
        if contracted_company is None and truck is not None:
            raise DRFValidationError({"truck":["Can not assign truck to load without company field"]})
        elif truck is not None and contracted_company is not None and truck.company != contracted_company:
            raise DRFValidationError({"truck":["is not part of contracted_company"]})
        
        ## check if trailer is part of contracted_company
        if contracted_company is None and trailer is not None:
            raise DRFValidationError({"trailer":["Can not assign trailer to load without company field"]})
        elif trailer is not None and contracted_company is not None and trailer.company != contracted_company:
            raise DRFValidationError({"trailer":["is not part of contracted_company"]})
        
        return super().validate(attrs)


    def create(self, validated_data):
        if validated_data.get('route',None) is None:
            raise DRFValidationError({"route":["route is null/missing. It must be a new route object."]})
        
        # assign company and contracted company if not assigned already        
        company = self.validate_company_create(validated_data.get('company',None)) 
        validated_data['company'] = company
        contracted_company = self.validate_contracted_company_create(validated_data.get('contracted_company',None))
        validated_data['contracted_company'] = contracted_company

        route_data = validated_data.pop('route',None)
        if route_data is not None:
            with transaction.atomic():
                route_serializer = RouteCreationSerializer(data=route_data, context={'request': self.context.get('request',None)})
                route_serializer.is_valid(raise_exception=True)
                new_route = route_serializer.save()
                return Load.objects.create(route=new_route,**validated_data)
        
    
    ## TODO: test update
    def update(self, instance, validated_data):
        if validated_data.get('route',None) is None:
            raise DRFValidationError({"route":["route is null/missing. It must be a new route object."]})
        
        # assign company and contracted company if not assigned already        
        company = self.validate_company_create(validated_data.get('company',None)) 
        if company is  None:
            validated_data['company'] = company
        contracted_company = self.validate_contracted_company_create(validated_data.get('contracted_company',None))
        if contracted_company is None:
            validated_data['contracted_company'] = contracted_company

        route_data = validated_data.pop('route',None)
        with transaction.atomic():
            if route_data is not None:
                ## delete old one
                if instance.route:
                    instance.route.delete() 
                ## create new one
                route_serializer = RouteCreationSerializer(data=route_data, context={'request': self.context.get('request',None)})
                route_serializer.is_valid(raise_exception=True)
                new_route = route_serializer.save()
                validated_data['route'] = new_route
                
            # update any other fields:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            
            return instance
    
    





