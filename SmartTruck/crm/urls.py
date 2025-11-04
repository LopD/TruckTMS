## django libs
from django.urls import path,include

## custom libs
from . import views

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('company', views.CompanyViewSet, basename='company')
router.register('company-industry', views.CompanyIndustryViewSet, basename='company-industry')



urlpatterns = [
    # path('test/', views.TestView.as_view(), name='test'),
] + router.urls