from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from owegoapi.models import BillTag, Bill, Tag, Owegouser
from django.contrib.auth import get_user_model
User = get_user_model()


class BillTagView(ViewSet):
    """Tag types"""



    def list(self, request):
        """Handle GET requests to get all categories
        Returns:
            Response -- JSON serialized list of categories
        """
        billTags = BillTag.objects.all()
        
        # bill = self.request.query_params.get('bill_id', None)
        # tags = tags.filter(bill__id=bill)

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = BillTagSerializer(
            billTags, many=True, context={'request': request})
        return Response(serializer.data)
    
    
class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags
    Arguments:
        serializers
    """
    class Meta:
        model = Tag
        fields = ('id', 'label')
    
class BillTagSerializer(serializers.ModelSerializer):
    """
    JSON Serialzer for BillTags
    Arguments:
        serializers
    """
    tag = TagSerializer(many=False)
    class Meta:
        model = Bill
        fields = ('id', 'tag')