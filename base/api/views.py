from rest_framework.decorators import api_view 
from rest_framework.response import Response 

# models : 
from base.models import Room 

# serializers : 
from . import serializers 

# --------------------------------------------------

# views : 
@api_view ( [ 'GET' ]) 
def getRoutes ( request ) : 

    routes = [

        'GET /api/' , 
        'GET /api/rooms' , 
        'GET /api/room/roomId' 
    ]

    return Response ( routes ) 


# --------------------------------

# get rooms view : 
@api_view ( [ 'GET' ]) 
def getRooms ( request ) : 

    rooms = Room.objects.all () 

    roomSerializer = serializers.RoomSerializer ( rooms, many = True )

    return Response (  roomSerializer.data )

# ----------------------------------------

# get room view : 
@api_view ( [ 'GET' ])
def getRoom ( request , roomId  ) : 

    room = Room.objects.get ( id = roomId ) 

    roomSerializer = serializers.RoomSerializer ( room ) 

    return Response ( roomSerializer.data ) 