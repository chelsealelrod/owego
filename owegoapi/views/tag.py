"""View module for handling requests about tags"""
# from nis import cat
# from unicodedata import tag
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from owegoapi.models import Tag, Owegouser, Bill
from django.contrib.auth import get_user_model
User = get_user_model()


class TagView(ViewSet):
    """Tag types"""
    
    def create(self, request):
        """Handle POST operations for tags
        Returns:
            Response -- JSON serialized tag instance
        """

        tag = Tag()
        tag.label = request.data["label"]


        try:
            tag.save()
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single tag
        Returns:
            Response -- JSON serialized tag
        """
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all categories
        Returns:
            Response -- JSON serialized list of categories
        """
        tags = Tag.objects.all()
        
        # bill = self.request.query_params.get('bill_id', None)
        # tags = tags.filter(bill__id=bill)

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = TagSerializer(
            tags, many=True, context={'request': request})
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        """Handle PUT requests for a tag
        Returns:
            Response -- Empty body with 204 status code
        """

        tag = Tag.objects.get(pk=pk)        
        tag.label = request.data["label"]
        
        tag.save()
        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single post
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            tag = Tag.objects.get(pk=pk)
            tag.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for tags
    Arguments:
        serializers
    """
    class Meta:
        model = Tag
        fields = ('id', 'label')
        
class TagUserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
class TagOwegoUserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer"""
    user = TagUserSerializer(many=False)

    class Meta:
        model = Owegouser
        fields = ['user']