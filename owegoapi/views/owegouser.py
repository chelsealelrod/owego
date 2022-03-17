from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers

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