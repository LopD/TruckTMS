"""
ASGI config for SmartTruck project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
## std
import os

## django
import django
from django.core.asgi import get_asgi_application

## channels
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

## tracking app
from tracking.websocket_urls import websocket_urlpatterns
from tracking.websocket_auth import JWTAuthMiddleware
# import tracking.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartTruck.settings')

## old:
# application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # "websocket": AuthMiddlewareStack(
    #     URLRouter(websocket_urlpatterns)
    # ),
    "websocket": JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})
