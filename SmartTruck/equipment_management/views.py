## django libs
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate   
from django.shortcuts import render
from django.db.models import Q
from django.db import transaction, IntegrityError
from django.db.models import Count
from django.core.exceptions import ValidationError as DjangoValidationError 

## rest framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes,action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework import permissions
from rest_framework.serializers import ValidationError as DRFValidationError
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser

## django_filters
from django_filters.rest_framework import DjangoFilterBackend

## core
from core.utilities.checks import request_auth_has_group, get_token_userid, get_request_file
from core.utilities.utils import str_to_bool

## 
from .models import *
from .serializers import *
from .permissions import *
from .filters import *


class TruckViewSet(viewsets.ModelViewSet):
    
    queryset = Truck.objects.all().order_by('pk')
    serializer_class = TruckSerializer
    permission_classes = [TruckPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter] ## SearchFilter
    filterset_class = TruckFilter
    search_fields = ['license_plate_number','vin'] 
    ordering_fields = ['pk','vin'] 
    ordering = ['pk']

    def get_queryset(self):
        
        ## Return all if user is admin
        if self.request.user.is_staff or self.request.user.is_superuser:
            return self.queryset
        
        user_id = self.request.user.id
        
        ## Return all loads based on the user role/group
        from core.utilities.checks import get_token_user_groups
        user_groups = get_token_user_groups(self.request)
        company_id = UserProfile.objects.filter(pk=user_id).values_list('company_id', flat=True).first()

        if 'Managers' in  user_groups:            
            return self.queryset.filter(company_id=company_id)
        elif 'Dispatchers' in  user_groups:            
            return self.queryset.filter(company_id=company_id)
        elif 'Drivers' in user_groups:     
            this_drivers_truck = self.queryset.filter(assigned_drivers=user_id)
            return this_drivers_truck
        else:
            return self.queryset

    def get_serializer_class(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return TruckCreationSerializer
        return self.serializer_class
    

    @action(
        detail=False,
        methods=["POST"],
        parser_classes=[MultiPartParser],
        url_path="import-csv",
    )
    def import_csv(self, request, **kwargs):
        ## Check that a file was provided
        
        try:
            uploaded_file = get_request_file(request=request, MAX_FILE_UPLOAD_SIZE_MB=25)
        except DjangoValidationError as e:
            raise DRFValidationError(e.message_dict)
        
        import pandas as pd
        
        try:
            df = pd.read_csv(uploaded_file, dtype=str, encoding='utf-8')
            df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
        except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError, ValueError) as e:
            return Response(
                {"error": f"Invalid CSV format: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
                
        ## replace np.nan (aka. NaN) values with python None
        df[df.isnull()] = None  ##inplace update, does not create a copy but changes all columns to 'object' which has a performance impact
        # print(df.head(10))

        ## https://dev.to/frankezenwanne/how-to-upload-a-csv-file-to-django-rest-28fo
        ## https://django.wtf/blog/file-uploads-with-django-drf/
        ## and the chatgpt convo

        bulk_data=[]        ## list of objects to be created in bulk
        errors = []         ## list of errors

        ## related data
        user_id = request.auth.get('user_id',None)
        if user_id is None:
            return Response(
                {"error": f"Invalid auth."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        company_id = Dispatcher.objects.filter(pk=user_id).values_list('company_id', flat=True).first()
        if company_id is None:
            return Response(
                {"error": f"Invalid auth. Dispatcher profile could not be found."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        ## NOTE:This creates an unsaved model instance with only the id set. 
        ## NOTE: Django will not query the database for this. It just uses the given primary key when saving. 
        ## NOTE: This means that a model with that ID must already exist in the database or you'll get a Database error
        truck_company = Company(id=company_id) 

        for index,row in df.iterrows():
            try:
                # Name,Phone Number,Email,DOT Number,MC Number,Website
                row_instance= Truck(    
                        company                               = truck_company, 
                        vin                                   = row.get('vin').strip().upper() if row.get('vin') is not None else "",
                        status                                = row.get('status').strip() if row.get('status') is not None else Truck._meta.get_field('status').get_default(),
                        license_plate_state_usps_abbreviation = row.get('license_plate_state_usps_abbreviation').strip().upper() if row.get('license_plate_state_usps_abbreviation') is not None else "",
                        license_plate_number                  = row.get('license_plate_number').strip() if row.get('license_plate_number') is not None else "",
                        is_leased                             = row.get('is_leased') if row.get('is_leased') is not None else Truck._meta.get_field('is_leased').get_default(),
                        lease_rate                            = row.get('lease_rate') if row.get('lease_rate') is not None else Truck._meta.get_field('lease_rate').get_default(),
                        is_active                             = row.get('is_active'),
                        weigth_lbs                            = row.get('weigth_lbs'),
                        length_ft                             = row.get('length_ft'),
                        )
                row_instance.full_clean()
                bulk_data.append(row_instance)
            except DjangoValidationError as e:
                errors.append({
                    "row_id": index+1,
                    "error": e.message_dict ## str(e)
                })
            except ValueError as e:
                errors.append({
                    "row_id": index+1,
                    "error": "Value error encountered!" ## TODO: make this error more clear to the user without giving away any info about our database
                })
            except Exception as e:
                message_dict = e.get(message_dict,None)
                errors.append({
                    "row_id": index+1,
                    "error": str(e) if (message_dict is None or message_dict == {}) else message_dict
                })
                
        
        ## raise as serializer error
        if errors:
            raise DRFValidationError(errors)
        
        try:
            with transaction.atomic():
                # pass
                Truck.objects.bulk_create(bulk_data) ## NOTE: bulk_create does not call save() nor clean() of the model instance. That must be done beforehand.
        except IntegrityError as e:
            return Response(
                {"error": "One or more companies could not be created due to duplicated or invalid data."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            try:
                import sys
                ## the below print statement does this: print(class_name.method_name ...)
                print(f"[Custom Log] {self.__class__.__name__}.{sys._getframe(0).f_code.co_name} encountered exception: {str(e)}")
            except Exception as e:
                pass
            return Response({"error": "Unknown exception occured" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"message" : "CSV file processed successfully"}, status=status.HTTP_201_CREATED)



class TrailerViewSet(viewsets.ModelViewSet):
    
    queryset = Trailer.objects.all().order_by('pk')
    serializer_class = TrailerSerializer
    permission_classes = [TrailerPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter] ## SearchFilter
    filterset_class = TrailerFilter
    search_fields = ['license_plate_number','vin'] 
    ordering_fields = ['pk','vin'] 
    ordering = ['pk']

    def get_queryset(self):
        
        ## Return all if user is admin
        if self.request.user.is_staff or self.request.user.is_superuser:
            return self.queryset
        
        user_id = self.request.user.id
        
        ## Return all loads based on the user role/group
        from core.utilities.checks import get_token_user_groups
        user_groups = get_token_user_groups(self.request)
        company_id = UserProfile.objects.filter(pk=user_id).values_list('company_id', flat=True).first()
        
        if 'Managers' in  user_groups:            
            return self.queryset.filter(company_id=company_id)
        elif 'Dispatchers' in  user_groups:            
            return self.queryset.filter(company_id=company_id)
        elif 'Drivers' in user_groups:     
            this_drivers_trailer = self.queryset.filter(assigned_drivers=user_id)
            return this_drivers_trailer
        else:
            return self.queryset

    def get_serializer_class(self):
        if self.request.method not in permissions.SAFE_METHODS:
            return TrailerCreationSerializer
        return self.serializer_class

