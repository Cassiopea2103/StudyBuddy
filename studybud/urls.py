
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse 

# handling media files : 
from django.conf import settings 
from django.conf.urls.static import static 

def home ( request ) : 

    return HttpResponse("Hello Zale! ") 

urlpatterns = [
    path('admin', admin.site.urls),
    path ('', include ('base.urls') ) , 
    path ( 'api/' , include ( 'base.api.urls' ))
]

# appending media url in url patterns : 
urlpatterns += static ( settings.MEDIA_URL , document_root = settings.MEDIA_ROOT )
