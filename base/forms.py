from django.forms import ModelForm 

# importing the models : 
from .models import Room 
from .models import User

from django.contrib.auth.forms import UserCreationForm


# -----------------------------------------------
# Room Form 
class RoomForm ( ModelForm ) : 

    class Meta : 
        model = Room 
        fields = '__all__'
        exclude = ['host' , 'participants']


# -----------------------------------------------

# UserForm 
class UserForm ( ModelForm ) : 
    class Meta : 
        model = User 
        fields = [
              'avatar' ,
            'username', 
            'name' , 
            'email' , 
            'bio'
        ]
        

# ------------------------------------------------

# MyUserCreationForm : 
class MyUserCreationForm ( UserCreationForm ) : 

    class Meta : 
        
        model = User 
        fields = [
            'username' ,
            'name', 
            'email', 
            'password1', 
            'password2'
        ]