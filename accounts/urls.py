from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import path

from accounts import forms,views
from . import views
app_name='account'
urlpatterns = [
  path('loginuser',views.LoginToken.as_view(),name='loginuser'),
  path('signup',views.signup,name='signup'),
  path('logoutapp',views.custom_logout.as_view(),name='logoutapp')
]
