## rest framework
from rest_framework import serializers
from rest_framework.serializers import ValidationError as DRFValidationError

## django lib
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError 
from django.db import transaction
from django.contrib.auth.models import Group

## django extensions
from ulid_django.converters import ULIDConverter

## custom models
from .models import *

## core
from core.models import UserProfile
from core.serializers import UserCreationSerializer, UserSerializer, UserProfileSerializer, RegisterSerializer

## geolocation
from geolocation.models import Location
from geolocation.serializers import LocationSerializer

## ulid
from ulid import ULID


class DispatcherSerializer(serializers.ModelSerializer):
    
    # user_profile = UserProfileSerializer(source='userprofile_ptr')
    user = UserSerializer(required=False)

    class Meta:
        model = Dispatcher
        fields = '__all__'
    
    def create(self, validated_data):
        raise DRFValidationError("Serialzier can not create objects")



class DispatcherUpdateSerializer(serializers.ModelSerializer):
    
    user = UserCreationSerializer(required=False)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(),required=False)

    class Meta:
        model = Dispatcher
        fields = '__all__'

    def update(self, instance, validated_data):

        # nested user update
        user_data = validated_data.pop('user', None)
        if user_data is None:
            user_data = validated_data.pop('user_profile',None)
        
        with transaction.atomic():
            if user_data:
                user_serializer = UserCreationSerializer(
                    instance=instance.user,
                    data=user_data,
                    partial=True
                )
                user_serializer.is_valid(raise_exception=True)
                user_serializer.save()

            # normal fields (company + dispatcher) can be updated directly:
            if 'company' in validated_data:
                instance.company = validated_data['company']

            # update any other driver fields:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance




class DispatcherCreationSerializer(serializers.ModelSerializer):
    
    user = UserCreationSerializer(required=True)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(),required=False)
    

    class Meta:
        model = Dispatcher
        fields = '__all__'
    

    def create(self, validated_data):

        request = self.context.get('request',None)
        
        company = validated_data.pop('company', None)
        if company is None and request is not None:
            profile = UserProfile.objects.filter(pk=request.user.id).first()
            company = profile.company
        if company is None:
            raise DRFValidationError({"company": ["company could not be found"]})

        user_data = validated_data.pop('user',None)
        if user_data is None:
            user_data = {
                'username'      : validated_data.pop('username', None),
                "email"         : validated_data.pop('email', None),
                'first_name'    : validated_data.pop('first_name', None),
                'last_name'     : validated_data.pop('last_name', None),
                'password'      : validated_data.pop('password', None),
            }
        
        ## create new Driver user
        with transaction.atomic():
            user_serializer = RegisterSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            new_user = user_serializer.save()
            try:
                user_group = Group.objects.get(name="Dispatchers")
            except Group.DoesNotExist:
                raise DRFValidationError({"auth_group": ["\'Dispatchers\' group does not exist."]})
            user_group.user_set.add(new_user)

            validated_data['user'] = new_user
            validated_data['company'] = company
            return super().create(validated_data)
    


class DriverSerializer(serializers.ModelSerializer):
    
    assigned_dispatcher = DispatcherSerializer()
    # user_profile = UserProfileSerializer(source='userprofile_ptr')
    user = UserSerializer(required=False)

    class Meta:
        model = Driver
        fields = '__all__'
    
    def create(self, validated_data):
        raise DRFValidationError("Serialzier can not create objects")
    


class DriverUpdateSerializer(serializers.ModelSerializer):
    
    user = UserCreationSerializer(required=False)
    assigned_dispatcher = serializers.PrimaryKeyRelatedField(queryset=Dispatcher.objects.all(),required=False)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(),required=False)

    class Meta:
        model = Driver
        fields = '__all__'

    def update(self, instance, validated_data):

        # nested user update
        user_data = validated_data.pop('user', None)
        if user_data is None:
            user_data = validated_data.pop('user_profile',None)
        
        with transaction.atomic():
            if user_data:
                user_serializer = UserCreationSerializer(
                    instance=instance.user,
                    data=user_data,
                    partial=True
                )
                user_serializer.is_valid(raise_exception=True)
                user_serializer.save()

            # normal fields (company + dispatcher) can be updated directly:
            if 'company' in validated_data:
                instance.company = validated_data['company']

            if 'assigned_dispatcher' in validated_data:
                instance.assigned_dispatcher = validated_data['assigned_dispatcher']

            # update any other driver fields:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance




class DriverCreationSerializer(serializers.ModelSerializer):
    
    user = UserCreationSerializer(required=False)
    assigned_dispatcher = serializers.PrimaryKeyRelatedField(queryset=Dispatcher.objects.all(),required=False)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(),required=False)

    class Meta:
        model = Driver
        fields = '__all__'



    def create(self, validated_data):

        request = self.context.get('request',None)
        
        assigned_dispatcher = validated_data.pop('assigned_dispatcher', None)
        if assigned_dispatcher is None and request is not None:
            try:
                assigned_dispatcher = Dispatcher.objects.filter(pk=request.user.id).first()
            except Dispatcher.DoesNotExist:
                raise DRFValidationError({"assigned_dispatcher": ["dispatcher could not be found. If you are a mangaer then you must select a valid dispatcher"]})
        
        company = validated_data.pop('company', None)
        if company is None and request is not None:
            profile = UserProfile.objects.filter(pk=request.user.id).first()
            company = profile.company
        if company is None:
            raise DRFValidationError({"company": ["company could not be found"]})

        user_data = validated_data.pop('user',None)
        if user_data is None:
            user_data = validated_data.pop('user_profile',None)
        if user_data is None:
            user_data = {
                'username'      : validated_data.pop('username', None),
                "email"         : validated_data.pop('email', None),
                'first_name'    : validated_data.pop('first_name', None),
                'last_name'     : validated_data.pop('last_name', None),
                'password'      : validated_data.pop('password', None),
            }
        
        ## create new Driver user
        with transaction.atomic():
            user_serializer = RegisterSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            new_user = user_serializer.save()
            try:
                user_group = Group.objects.get(name="Drivers")
            except Group.DoesNotExist:
                raise DRFValidationError({"auth_group": ["\'Drivers\' group does not exist."]})
            user_group.user_set.add(new_user)

            validated_data['user'] = new_user
            validated_data['company'] = company
            validated_data['assigned_dispatcher'] = assigned_dispatcher
            return super().create(validated_data,)
    




class ManagerSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(required=False)

    class Meta:
        model = Manager
        fields = '__all__'
    
    def create(self, validated_data):
        raise DRFValidationError("Serialzier can not create objects")



class ManagerUpdateSerializer(serializers.ModelSerializer):
    
    user = UserCreationSerializer(required=False)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(),required=False)

    class Meta:
        model = Manager
        fields = '__all__'

    def update(self, instance, validated_data):

        # nested user update
        user_data = validated_data.pop('user', None)
        if user_data is None:
            user_data = validated_data.pop('user_profile',None)
        
        with transaction.atomic():
            if user_data:
                user_serializer = UserCreationSerializer(
                    instance=instance.user,
                    data=user_data,
                    partial=True
                )
                user_serializer.is_valid(raise_exception=True)
                user_serializer.save()

            # normal fields (company + dispatcher) can be updated directly:
            if 'company' in validated_data:
                instance.company = validated_data['company']

            # update any other driver fields:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance




class ManagerCreationSerializer(serializers.ModelSerializer):
    
    user = UserCreationSerializer(required=True)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(),required=False)
    

    class Meta:
        model = Manager
        fields = '__all__'
    

    def create(self, validated_data):

        request = self.context.get('request',None)
        
        company = validated_data.pop('company', None)
        if company is None and request is not None:
            profile = UserProfile.objects.filter(pk=request.user.id).first()
            company = profile.company
        if company is None:
            raise DRFValidationError({"company": ["company could not be found"]})

        user_data = validated_data.pop('user',None)
        if user_data is None:
            user_data = {
                'username'      : validated_data.pop('username', None),
                "email"         : validated_data.pop('email', None),
                'first_name'    : validated_data.pop('first_name', None),
                'last_name'     : validated_data.pop('last_name', None),
                'password'      : validated_data.pop('password', None),
            }
        
        ## create new Driver user
        with transaction.atomic():
            user_serializer = RegisterSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            new_user = user_serializer.save()
            try:
                user_group = Group.objects.get(name="Managers")
            except Group.DoesNotExist:
                raise DRFValidationError({"auth_group": ["\'Managers\' group does not exist."]})
            user_group.user_set.add(new_user)

            validated_data['user'] = new_user
            validated_data['company'] = company
            return super().create(validated_data)
