from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls',namespace='accounts')),
   
     path('reservation/',include('reservation.urls',namespace='reservation')),
    path('home/',include('home.urls',namespace='home')),
    path('notifcation/',include('notifcation.urls',namespace='notifcation')),
    
]
urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
