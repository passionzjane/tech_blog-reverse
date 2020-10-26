from django.urls import path
from django.contrib import admin
from .views import (
    UserCreateAPIView,
    UserLoginAPIView,
)

app_name = 'accounts'

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),

]
