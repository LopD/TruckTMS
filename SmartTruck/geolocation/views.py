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

##
from .models import *
from .serializers import *
# from .permissions import *
# from .filters import *


class LocationViewSet(viewsets.ModelViewSet):

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    # permission_classes = [LoadPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter] ## SearchFilter
    # filterset_class = LoadFilter
    search_fields = [] ## 'route__from_location__city_name',
    ordering_fields = ['pk'] 
    ordering = ['-pk']     

    def get_queryset(self):
        return self.queryset

    def get_serializer_class(self):
        return self.serializer_class
