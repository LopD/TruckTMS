## django libs
from django.urls import path,include

## custom libs
from . import views

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# router.register(r'load', views.LoadViewSet, basename='load')
router.register('driver', views.DriverViewSet, basename='driver')
router.register('dispatcher', views.DispatcherViewSet, basename='dispatcher')



urlpatterns = [
] + router.urls 