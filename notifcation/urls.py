from django.urls import path
from rest_framework import routers
 
from . import views
app_name='notifcation'
urlpatterns = [

  #send notification 
  path('', views.send_note,name='notefication'),
  path('create_note', views.note_create,name='create_note'),
  path('delete_note/<uuid:unique_id>', views.delete_note,name='delete_note'),
  path('notes', views.Notes.as_view(),name='notes'),
  path('noteprivate', views.Noteprivate.as_view(),name='noteprivate'),  
]
