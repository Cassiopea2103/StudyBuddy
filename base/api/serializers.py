from rest_framework.serializers import ModelSerializer 

# models : 
from base.models import Room 

#  creating serializers : 

# -------------------------------------

# room serializer : 
class RoomSerializer ( ModelSerializer ) : 

    class Meta : 
        model = Room 
        fields = '__all__'