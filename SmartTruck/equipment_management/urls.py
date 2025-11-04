## django libs
from django.urls import path,include

## custom libs
from . import views

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# router.register(r'load', views.LoadViewSet, basename='load')
router.register('truck', views.TruckViewSet, basename='truck')
router.register('trailer', views.TrailerViewSet, basename='trailer')



urlpatterns = [
] + router.urls 