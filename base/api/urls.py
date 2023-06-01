from django.urls import path 

from . import views 

urlpatterns = [

    path ( '' , views.getRoutes ), 
    path ( 'rooms' , views.getRooms ), 
    path ( 'room/<str:roomId>' , views.getRoom)
]