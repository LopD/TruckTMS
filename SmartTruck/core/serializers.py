## rest framework
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError as DRFValidationError

## django lib
from django.contrib.auth import get_user_model

## custom models
from .models import UserProfile


'''
    Creates a custom auth token for the given user
'''
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['groups'] = list(user.groups.values_list('name', flat=True))

        return token



'''
    Registers a new user.
'''
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    # Example: individual field validation
    def validate_email(self, value):
        import re
        email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        if not bool(email_regex.match(value)):
            raise serializers.ValidationError("Email is invalid.")
        if get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already registered.")
        return value

    def validate_username(self, value):
        if get_user_model().objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is taken.")
        return value

    def validate_first_name(self, value):
        if not isinstance(value,str) or len(value) <= 0:
            raise serializers.ValidationError("First name can not be empty.")
        return value
    
    def validate_last_name(self, value):
        if not isinstance(value,str) or len(value) <= 0:
            raise serializers.ValidationError("Last name can not be empty.")
        return value

    def create(self, validated_data):
        ## create user
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_active=True  ## TODO: Don't allow login until confirmed
        )

        return user
    

'''
    Registers a new Profile for the new user.
'''
class RegisterProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'
    
    def validate_user(self, value):
        if UserProfile.objects.filter(user=value).exists():
            raise serializers.ValidationError("user already has a profile.")
        if not get_user_model().objects.filter(pk=value.id).exists():
            raise serializers.ValidationError("user does not exist.")
        return value

    def create(self, validated_data):
        profile = UserProfile.objects.create(
            user=validated_data['user'],
            company=validated_data['company'],
            ## TODO: add this back
            # is_email_verified=validated_data.get('is_email_verified',UserProfile._meta.get_field('is_email_verified').get_default()),
            is_email_verified=True,
        )
        return profile
    

class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        raise DRFValidationError("Serialzier can not create objects")

    class Meta:
        model = get_user_model()
        # Pick the fields you want to expose
        exclude = ['password','groups','user_permissions']



class UserCreationSerializer(serializers.ModelSerializer):
    """
    NOTE: is_staff, is_superuser is exposed
    """
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def validate(self, attrs):
        return super().validate(attrs)

    class Meta:
        model = get_user_model()
        # Pick the fields you want to expose
        exclude = ['date_joined','last_login']



class UserProfileSerializer(serializers.ModelSerializer):
    """
    Only used for displaying
    """
    user = UserSerializer()

    def create(self, validated_data):
        raise DRFValidationError("Serialzier can not create objects")

    class Meta:
        model = UserProfile
        fields = '__all__'



class UserProfileCreationSerializer(serializers.ModelSerializer):

    user = UserCreationSerializer()

    def create(self, validated_data):

        user_data = validated_data.pop('user',None)
        if user_data is None:
            raise DRFValidationError({'user':['Object is missing']})
    
        user_serializer = UserCreationSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        new_user = user_serializer.save()
        return self.Meta.model.objects.create(**validated_data, user=new_user)
        # return super().create(**validated_data)

    class Meta:
        model = UserProfile
        fields= '__all__'

