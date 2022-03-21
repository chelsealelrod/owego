from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from owegoapi.models import Owegouser


@api_view( ['GET'])
def get_owegouser_profile(request):
    """
    Get Owegouser
    """
    owegouser = request.auth.user.owegouser
        
    serializer = OwegouserSerializer(owegouser, context={'request': request})
        
    return Response(serializer.data)
    

class OwegouserSerializer(serializers.ModelSerializer):
    """
    OwgoUser
    """
    
    class Meta:
        model = Owegouser
        fields = ('user')
        
class BillUserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        