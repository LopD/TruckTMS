## django 
from django.urls import path

## 
from . import consumers

websocket_urlpatterns = [
    path("ws/vehicle-tracking/", consumers.VehicleTrackingConsumer.as_asgi()),
]
