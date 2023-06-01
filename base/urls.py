from django.urls import path 

# importing the views : 

from . import views 

urlpatterns = [ 

    path ( 'login', views.loginPage, name = 'login'),
    path ( 'logout', views.logoutPage , name = 'logout' ) , 
    path ( 'register', views.registerPage, name = 'register' ) , 
    path ('', views.home , name = 'homepage' ), 
    path ( 'rooms/<str:roomId>', views.room , name = 'rooms' ) ,
    path ( 'create-room/', views.create_room , name = 'create_room' ),
    path ( 'update-room/<str:roomId>', views.updateRoom , name = 'update_room' ),
    path ( 'delete-room/<str:roomId>' , views.deleteRoom, name= 'delete_room' ),
    path ( 'deleteMessage/<str:messageId>', views.deleteMessage, name = 'deleteMessage'),
    path ( 'userProfile/<str:userId>/' , views.userProfile, name = 'userProfile' ), 
    path ( 'upateUser/<str:userId>/', views.updateUser, name = 'updateUser' ) , 
    path ( 'topicsPage' , views.topicsPage, name = 'topicsPage'), 
    path ( 'activities', views.activities , name = 'activities' )
]