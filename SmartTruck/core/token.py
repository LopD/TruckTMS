# accounts/tokens.py
from rest_framework_simplejwt.tokens import Token
from datetime import timedelta
from django.conf import settings

'''
    Token sent to the users email when signing up. The user uses this token to verify his email in order to gain access to our site.
'''
class EmailVerificationToken(Token):
    lifetime = timedelta(days=7)  # Change this to your preferred expiry (e.g., 10 minutes)
    token_type = 'email'
    lifetime_claim = 'email_exp'



'''
    Custom encoded 
'''
# from rest_framework_simplejwt.tokens import AccessToken

# class CustomAccessToken(AccessToken):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         user = self['user_id']
#         from django.contrib.auth import get_user_model
#         User = get_user_model()
#         instance = User.objects.get(id=user)
#         self['groups'] = [group.name for group in instance.groups]
#         self['email'] = instance.email
#         # self['permissions'] = list(instance.get_all_permissions())
