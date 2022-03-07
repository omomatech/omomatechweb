from django.urls import path
from rest_framework import routers
 
from . import views
app_name='reservation'
urlpatterns = [


  path('reservation', views.getlistdayreservation,name='reservation'),
  path('create_reservation', views.create_reservation.as_view(),name='create_reservation'),
  path('reservation_list', views.reservation_list.as_view(),name='reservation_list'),

   
]
