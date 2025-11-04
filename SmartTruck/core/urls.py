## django libs
from django.urls import path,include

## custom libs
from . import views
from .views import *


## rest framework libs
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

# router.register(r'load', views.LoadViewSet, basename='load')
router.register('user', views.UserViewSet, basename='user')
# router.register('route', views.RouteViewSet, basename='route')

urlpatterns = [
    path('log-in/', views.LogIn.as_view() ),
    path('log-out/', views.LogOut.as_view()),
    path('sign-up/', views.SignUp.as_view()),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('email-verify/', views.VerifyEmail.as_view(), name='email-verify'),
] + router.urls