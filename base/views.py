from django.shortcuts import render, redirect
from django.db.models import Q
# Create your views here.

# importing the models : 
from .models import Room
from .models import Topic
from .models import Message
from .models import User 


# login/registration related imports 
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm , MyUserCreationForm

# flash messages : 
from django.contrib import messages 


# importing the model forms : 
from .forms import RoomForm

# login/register view : 
def loginPage ( request ) : 

    if request.user.is_authenticated : 
        return redirect ( 'homepage' ) 
    

    if request.method == 'POST' : 
        # retrieve request data : 
        username = request.POST.get ('username').lower() 
        password = request.POST.get ( 'password' ) 

        try : 
            # check for user existence : 
            user = User.objects.get ( username = username ) 


            # certify user credentials ( like in a cookie ! )
            user = authenticate (
                request, 
                username = username , 
                password = password 
            )

            # now login the user : 
            if user is not None : 
                login ( request, user )
                return redirect ( 'homepage' )
            
            else : 
                # username or password are wrong: 
                messages.error ( request, 'Wrong username or password !')

        
        except : 
            messages.error ( request, 'User does not exist !' )

        

    return render ( request, 'base/login.html' )

# ----------------------------------------------------------------------------

# register view : 
def registerPage ( request ) : 

    form = MyUserCreationForm () 

    if request.method == 'POST' : 
        
        form = MyUserCreationForm ( request.POST ) 
        
    
        if form.is_valid () : 
        
            # register the user
            user = form.save( commit = False ) 
            user.username = user.username.lower()
            user.save () 
             
            # log him at the same time : 
            login ( request, user ) 

            # redirect him to the homepage : 
            return redirect ( 'homepage' ) 
        
        else : 
            messages.error ( request, 'An error occured during user registration! ')

    context = {
        'form': form 
    }

    return render ( request, 'base/register.html', context )

# ----------------------------------------------------------------------------

# logout view : 
def logoutPage ( request ) : 

    logout ( request )

    return redirect ( 'homepage' )

# -------------------------------------------------------------


# update user view : 
def updateUser ( request, userId ) : 

    user = User.objects.get ( id = userId )

    form = UserForm ( instance = user ) 

    if request.method == 'POST' : 
        
        form = UserForm ( request.POST , request.FILES , instance = user )

        if form.is_valid () : 

            form.save () 
            return redirect ( 'userProfile' , userId = user.id  ) 

    context = { 
        'form' : form 
    }

    return render ( request, 'base/updateUser.html', context )



#-----------------------------------------------------------------------------

# home view : 
def home ( request ) :

    # topics : 
    topics = Topic.objects.all () [ 0 : 4 ]

    # request topic query : 
    query = request.GET.get('query') if request.GET.get('query') != None else ''

    # rooms : 
    rooms = Room.objects.filter( 
        Q( topic__name__icontains = query ) | 
        Q ( name__icontains = query ) 
     )
    
    room_count = rooms.count() 

    room_messages= Message.objects.filter(
        Q( room__topic__name__icontains = query )
    ).order_by ( '-created')

    context = { 
        'rooms' : rooms,
        'topics' : topics,
        'room_count': room_count,
        'room_messages' : room_messages

    }

    return render ( request , 'base/home.html' , context )


# -----------------------------------------------------------------------------

# room view : 
def room ( request, roomId ) : 

    room = Room.objects.get ( id = roomId )

    room_messages = room.message_set.all().order_by ( '-created' ) 

    participants = room.participants.all () 

    # handling  message creation : 
    if request.method == 'POST' : 
        Message.objects.create ( 
            user = request.user, 
            room = room, 
            body = request.POST.get ( 'message_input' )
        )

        room.participants.add ( request.user ) 

        return redirect ( 'rooms', roomId = room.id )

    context = { 
        'room' : room, 
        'room_messages' : room_messages,
        'participants' : participants 
    }

    return render ( request , 'base/room.html' , context )


# ------------------------------------------------------------------------
@login_required ( login_url = 'login_register')
def create_room ( request ) : 


    topics = Topic.objects.all () 

    context= {
        'topics' : topics 
    }

    # handle the submit of form : 
    if request.method == 'POST' : 
        
        topic_name = request.POST.get ( 'topic' ) 
        topic, created = Topic.objects.get_or_create ( name = topic_name ) 

        new_room = Room.objects.create ( 
            name = request.POST.get ( 'room_name' ),
            host = request.user ,
            topic = topic , 
            description = request.POST.get ( 'description' ) 
        )

        new_room.participants.add ( request.user )

        return redirect ( 'homepage' )

    return render ( request, 'base/room-form.html', context )


# ---------------------------------------------------------
@login_required ( login_url = 'login_register' )
def updateRoom ( request, roomId ) : 

    # querying the room to update : 
    room = Room.objects.get ( id = roomId ) 

    topics = Topic.objects.all()

    if request.method == 'POST' :
        
        topic_name = request.POST.get ( 'topic' ) 
        topic, created = Topic.objects.get_or_create ( name = topic_name ) 

        room.name = request.POST.get ( 'room_name')
        room.host = request.user 
        room.topic = topic 
        room.description = request.POST.get ( 'room_description' ) 

        room.save () 

        return redirect ( 'homepage' ) 
    
    context = {
        'topics' : topics , 
        'room' : room
    }

    return render ( request, 'base/room-form.html', context )


# ---------------------------------------------------------------

@login_required ( login_url = 'login_register' )
def deleteRoom ( request , roomId ) : 

    # querying the room : 
    room = Room.objects.get ( id = roomId ) 

    context = { 
        'room' : room 
    }

    if request.method == 'POST' : 
        room.delete ()
        return redirect ( 'homepage' )

    return render ( request , 'base/delete-form.html', context )

# -----------------------------------------------------------------------------

# delete message view : 
def deleteMessage ( request, messageId ) : 

    room_message= Message.objects.get ( id = messageId ) 

    context = { 
        'room_message' : room_message 
    }
    if request.method == 'POST' : 
        room_message.delete() 

        return redirect ( 'rooms' , room_message.room.id )

    return render ( request, 'base/deleteMessage.html', context )

# -----------------------------------------------------------------------

# userProfile view : 
def userProfile ( request, userId ) : 

    user = User.objects.get ( id = userId )
    topics = Topic.objects.all () 
    rooms = user.room_set.all() 
    room_messages = user.message_set.all () 

    context = { 
        "user" : user ,
        'topics' : topics , 
        'rooms' : rooms ,
        'room_messages' : room_messages
    }

    return render ( request, 'base/profile.html' , context )

#---------------------------------------------------------------

# topics view : 
def topicsPage ( request ) : 

    query = request.GET.get ('query') if request.GET.get ( 'query' ) != None else  ''
    
    topics = Topic.objects.filter ( 
        Q ( name__icontains = query )
    ) 

    context = {
        'topics' : topics
    }

    return render ( request, 'base/topics.html' , context )

# -------------------------------------------------------

# activities view : 
def activities ( request ) :

    query = request.GET.get('query') if request.GET.get('query') != None else '' 

    room_messages= Message.objects.filter(
        Q( room__topic__name__icontains = query )
    ).order_by ( '-created')

    context = {
        'room_messages' : room_messages 
    }

    return render ( request, 'base/activity.html' , context )

