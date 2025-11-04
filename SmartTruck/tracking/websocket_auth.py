## 3rd party
import jwt
from urllib.parse import parse_qs

## django
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.response import Response

## rest_framework
from rest_framework_simplejwt.tokens import UntypedToken,AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

## channels
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

## core app
# from core.utilities.checks import get_token_user_groups

User = get_user_model()

@database_sync_to_async
def get_user(validated_token):
    try:
        user_id = validated_token.get("user_id")
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


class JWTAuthMiddleware(BaseMiddleware):
    '''
    Checks if a token is sent and if that token is valid.
    The permissions are handled on a view level.
    Adds the "user" and "groups" to the scope to represent the current user and his user groups.
    '''
    # def get_user_groups(validated_token):
    #     groups = validated_token.get("groups",[])
    #     return groups

    
    async def __call__(self, scope, receive, send):
        """
        Checks if a token is sent and if that token is valid.
        Adds the "user" and "groups" to the scope to represent the current user and his user groups.
        """
        try:
            query_string = parse_qs(scope["query_string"].decode())
            token = query_string.get("token", [None])[0]
            if token is None:
                raise TokenError("No token provided")

            # validated_token = UntypedToken(token)
            validated_token = AccessToken(token)
            scope["user"] = await get_user(validated_token)
            # scope["groups"] = self.get_user_groups(token)
            scope["groups"] = validated_token.get("groups",[])

            
        except (InvalidToken, TokenError):
            ## set the user to None so he gets de authenticated 
            scope["user"] = None
            scope["groups"] = []

        return await super().__call__(scope, receive, send)
