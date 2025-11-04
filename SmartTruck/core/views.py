## python libs
import jwt, datetime

## django libs
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate   
from django.contrib.auth.models import Group  
from django.db import transaction

## rest framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes,action
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

## django_filters
from django_filters.rest_framework import DjangoFilterBackend

## crm
from crm.models import Company

from .serializers import *

# Create your views here.

'''
    Returns custom tokens
'''
from .serializers import CustomTokenObtainPairSerializer
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class LogOut(APIView): 

    @permission_classes([IsAuthenticated]) ## profile is active         
    def post(self,request,format=None):

        response = Response(status=200)
        response.data = {
            'message' : 'success'
        }
        return response



class LogIn(APIView):    
    
    ## TODO: add this back
    def has_verified_email(self,user):
        return True
        from .models import UserProfile
        user_profile = UserProfile.objects.get(user=user)
        if user_profile is None:
            return False
        return user_profile.is_email_verified
    
    @permission_classes([])
    def post(self,request,format=None):

        email = request.data['email']
        password = request.data['password']

        ## check if the email or password are blank
        if email is None or password is None or len(email) <= 0 or not isinstance(email,str) or len(password) <= 0 or not isinstance(password,str):
            return Response(status=400,data={'message':'email or password is empty or not a string!'})

        user = authenticate(email=email, password=password)
        # user = authenticate(username=user.username, password=password) ## can also be used
        if user is None:
            ## No backend authenticated the credentials
            return Response(status=404,data={'message':'User not found!'})
        ##else: A backend authenticated the credentials

        ## Check if the user has verified his email
        if not self.has_verified_email(user):
            return Response({'message':'Email is not verified!'}, status=status.HTTP_401_UNAUTHORIZED)

        ## create a JWT token for the user using his credentials
        username = user.username
        password = user.password
        serializer = CustomTokenObtainPairSerializer(data={
            "username": username,
            "password": password
        })
        if not serializer.is_valid(): 
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        
        # serializer.validated_data => Returns the token pair (access + refresh)
        # return Response(serializer.validated_data, status=status.HTTP_200_OK)    
        response = Response()
        response.data = serializer.validated_data
        response.data['message'] = 'success'

        ## update last login field
        user.last_login = datetime.datetime.now()
        user.save(update_fields=['last_login'])

        return response




'''
    Registers/signs up a new user
'''
class SignUp(APIView):
    
    @transaction.atomic
    def post(self, request):
        ## Try to create a new user
        from .serializers import RegisterSerializer,RegisterProfileSerializer
        from crm.serializers import CompanySerializer,CompanyCreationSerializer
        from user_management.models import Manager
        request_data = request.data
        
        ## get company name
        company_name = request_data.get('company_name',None)
        if company_name is None or not isinstance(company_name,str):
            company_name = request_data.get('company',None)
        if not isinstance(company_name,str):
            raise ValidationError({'': ['set \'company\' to a valid company name']})

        register_serializer_data = {k: v for k, v in request.data.items() if (k != 'company_name')}
        register_user_serializer = RegisterSerializer(data=register_serializer_data, context={'request': request})
        comapny_serializer = CompanyCreationSerializer(data={"name":company_name}, context={'request': request})

        with transaction.atomic():
            ## create user and company
            register_user_serializer.is_valid(raise_exception=True)
            comapny_serializer.is_valid(raise_exception=True)
            new_user = register_user_serializer.save()
            new_company = comapny_serializer.save()
            
            try:
                user_group = Group.objects.get(name="Managers")
            except Group.DoesNotExist:
                raise ValidationError({"auth_group": ["\'Managers\' group does not exist."]})
            user_group.user_set.add(new_user)

            ## create manager profile
            new_manager = Manager.objects.create(
                user = new_user,
                company = new_company
            )

            ## send verification email
            if new_user is not None and isinstance(new_user,get_user_model()):
                from .utilities.email.verificiation import VerificationEmailSender
                VerificationEmailSender.send(user=new_user)
            return Response(
                {'message': 'Registration successful. Please check your email to verify your account.'},
                status=status.HTTP_201_CREATED
            )
    
        ## or this response
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




'''
    Email verification link endpoint. 
'''
class VerifyEmail(APIView):

    def get(self, request):
        ## read token from query
        token = request.GET.get('token')
        try:
            ## update the user, set his status to active 
            from rest_framework_simplejwt.tokens import UntypedToken
            access_token = UntypedToken(token)
            user_id = access_token['user_id']
            user = get_user_model().objects.get(id=user_id)
            user.is_active = True
            
            ## verify his email
            from .models import UserProfile
            user_profile = UserProfile.objects.get(user=user)
            if user_profile is not None:
                user_profile.is_email_verified = True
                user_profile.save()

            user.save()

            ## take the custom auth token and send it back
            serializer = CustomTokenObtainPairSerializer(data={
                "username": user.username,
                "password": user.password
            })
            if not serializer.is_valid(): 
                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
            
            ## response
            response = Response()
            response.data = serializer.validated_data
            response['message'] = 'Email verified successfully!'
            response.status_code = status.HTTP_200_OK
            return response
        
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)



class UserViewSet(viewsets.ModelViewSet):
    
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = [CompanyIndustryPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter,SearchFilter] ## SearchFilter
    # filterset_class = CompanyIndustryFilter
    # search_fields = ['name'] ## 'route__from_location__city_name',
    # ordering_fields = ['pk','name'] 
    # ordering = ['pk','name']


    def get_queryset(self):
        return self.queryset

    def get_serializer_class(self):
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        """
        Handle complex query paramaters from the request.
        """
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        raise ValidationError("Can not create users this way")