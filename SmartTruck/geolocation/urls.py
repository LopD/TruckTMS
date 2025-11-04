## django libs
from django.urls import path,include

## custom libs
from . import views

from rest_framework.routers import DefaultRouter
router = DefaultRouter()


router.register('location', views.LocationViewSet, basename='location')


urlpatterns = [
] + router.urls 