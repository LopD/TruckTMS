## django libs
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate   
from django.shortcuts import render
from django.db.models import Q
from django.db import transaction, IntegrityError

## rest framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes,action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions,BasePermission
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.serializers import ValidationError as DRFValidationError
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser

## django_filters
from django_filters.rest_framework import DjangoFilterBackend

## core
from core.utilities.checks import request_auth_has_group, get_token_userid, get_request_file
from core.utilities.utils import str_to_bool

## crm
from .models import *
from .serializers import *
from .permissions import *
from .filters import *

# Create your views here.

class CompanyViewSet(viewsets.ModelViewSet):
    
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # pagination_class = LoadNumberPagination ## use the default paginaton class defined in settings.py
    permission_classes = [CompanyPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter] ## SearchFilter
    filterset_class = CompanyFilter
    search_fields = ['name','mc_number','dot_number'] ## 'route__from_location__city_name',
    ordering_fields = ['id','name','updated_at']
    ordering = ['id']


    def get_queryset(self):
        if self.action == "select":
            only_used_fields = self.search_fields + self.ordering_fields + self.ordering
            return Company.objects.only(*only_used_fields)
        return self.queryset

    def get_serializer_class(self):
        if self.request.method in ['POST','PUT']:
            return CompanyCreationSerializer

        return self.serializer_class

    def list(self, request, *args, **kwargs):
        """
        Handle complex query paramaters from the request.
        """
        return super().list(request, *args, **kwargs)

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

        for index,row in df.iterrows():
            try:
                # Name,Phone Number,Email,DOT Number,MC Number,Website
                row_instance= Company(
                        name            = row.get('Name').strip() if row.get('Name') is not None else row.get('Name'),
                        phone_number    = row.get('Phone Number'),
                        email           = row.get('Email'),
                        dot_number      = row.get('DOT Number').strip() if row.get('DOT Number') is not None else row.get('DOT Number'),
                        mc_number       = row.get('MC Number').strip() if row.get('MC Number') is not None else row.get('MC Number'),
                        website         = row.get('Website')
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
                Company.objects.bulk_create(bulk_data) ## NOTE: bulk_create does not call save() nor clean() of the model instance. That must be done beforehand.
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
    

    @action(
            detail=False, 
            methods=["GET"],
            url_path="select",
    )
    def select(self, request):
        from core.utilities.utils import QueryLogger
        only_used_fields = list(set(self.search_fields + self.ordering_fields + self.ordering))
        
        ## manually apply pagination and filtering
        ## 4 selects (2 data 1 count and 2 for filtering. need to optimize filtering in order to get best perfomance). for example: here I'm getting the Dispatcher of the profile twice since they're not in the same function
        # with QueryLogger(): 
        #     qs = Company.objects.values(*only_used_fields)
        #     qs = self.filter_queryset(qs)
        #     page = self.paginate_queryset(qs)
        #     if page is not None:
        #         # serializer = CompanySelectionSerializer(page, many=True)
        #         return self.get_paginated_response(page)
        

        qs = Company.objects.values(*only_used_fields)
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(page)
        


class CompanyIndustryViewSet(viewsets.ModelViewSet):
    
    queryset = CompanyIndustry.objects.all()
    serializer_class = CompanyIndustrySerializer
    # pagination_class = LoadNumberPagination ## use the default paginaton class defined in settings.py
    permission_classes = [CompanyIndustryPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter,SearchFilter] ## SearchFilter
    filterset_class = CompanyIndustryFilter
    search_fields = ['name'] ## 'route__from_location__city_name',
    ordering_fields = ['pk','name'] 
    ordering = ['pk','name']


    def get_queryset(self):
        return self.queryset

    def get_serializer_class(self):
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        """
        Handle complex query paramaters from the request.
        """
        return super().list(request, *args, **kwargs)
    