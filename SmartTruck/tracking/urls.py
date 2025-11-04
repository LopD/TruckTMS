## django libs
from django.urls import path,include

## custom libs
from . import views

## 
from .websocket_urls import websocket_urlpatterns


urlpatterns = [
] + websocket_urlpatterns