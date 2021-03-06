from webbrowser import get
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from owegoapi.models import Category, Owegouser
from django.contrib.auth import get_user_model
User = get_user_model()


class CategoryView(ViewSet):
    # permission_classes' = [IsAdminUser] has Objects.permissions
    """ categories"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single category

        Returns:
            Response -- JSON serialized category
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(
                category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """
        List of Categories
        """


        # @action(methods=['post', 'delete'], detail=True)
        # Get all game records from the database
        categories = Category.objects.all()

        # Support filtering posts by category
        #    http://localhost:8000/posts?category=1
        #
        # That URL will retrieve all tabletop posts

        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized a category instance
        """

        # Uses the token passed in the `Authorization` header
        category = Category()

        # Create a new Python instance of the Post class
        # and set its properties from what was sent in the
        # body of the request from the client.

        category.label = request.data["label"]

        # category = Category.objects.get(pk=request.data["category"])
        # category.category = category

        try:
            category.save()
            serializer = CategorySerializer(
                category, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        
        """Handle DELETE requests for a single category

        Returns:
            Response -- 200, 404, or 500 status code
        """
# this makes it so that we can only delete if we are admin/authorized
        try:
            category = Category.objects.get(pk=pk)
            category.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories

    Arguments:
        serializers
    """
    class Meta:
        model = Category
        fields = ('id', 'label')
        
class CategoryUserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
class CategoryOwegoUserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer"""
    user = CategoryUserSerializer(many=False)

    class Meta:
        model = Owegouser
        fields = ['user']
