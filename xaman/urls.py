from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from app.views import *
urlpatterns = [
  path('api/register', Register.as_view(), name='register'),
  path('api/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('api/login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
  path('api/login/verify', TokenVerifyView.as_view(), name='token_verify'),
  path('api/auth/datasets', Dataset.as_view(), name='datasets'),
]
