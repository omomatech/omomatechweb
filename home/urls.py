from django.urls import path

from . import views
app_name='home'
urlpatterns = [
   #path to function decide if user or admin
   path('homepage',views.homepage,name='homepage'),
   #path admin action(render) ==admin only
   path('home',views.create_profile,name='home'),
   #path to profile update page(render) ==admin only
   path('profileupdate/<uuid:unique_id>',views.profileupdate,name='profileupdate'),
   #path to add visiting page that pass profile uuid(render) ==admin only
   path('addvisiting/<uuid:unique_id>',views.addvisiting,name='addvisiting'),
   #path to addvisiting page to remove visiting pass visiting uuid(render) ==admin only
   path('delete_visitng/<uuid:unique_id>',views.delete_visitng,name='deletevisitng'),
   #path to delete image from visiting by uuid of image ==admin only
   path('deleteimage/<uuid:unique_id>',views.deleteimage,name='deleteimage'),
   #path to upload page images(render) ==admin
   path('uploadimages/<uuid:unique_id>',views.uploadimages,name='uploadimages'),
   #path to function that return list of (json) all visiting of profile login  ==user
   path('homeuser',views.ListVisting.as_view(),name='homeuser'),
   #path to function that return all image of visiting of profile by uuid of visiting login  Response(Json)  ==user
   path('Img_Visiting',views.Img_Visiting.as_view(),name='Img_Visiting'),
   path('print',views.profileprint,name='print'),
   


   
]
