from tkinter.ttk import Notebook
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from owegoapi.models import Note,Owegouser,Tag, Bill
from django.contrib.auth import get_user_model
User = get_user_model()

class NoteView(ViewSet):
    """Note posts"""

    def list(self, request):

        # Get all game records from the database
        notes = Note.objects.all() 
        
        bill = self.request.query_params.get('bill_id', None)
        notes = notes.filter(bill__id=bill)


        serializer = NoteSerializer(
            notes, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/notes/2
            #
            # The `2` at the end of the route becomes `pk`
            note = Note.objects.get(pk=pk)
            serializer = NoteSerializer(note, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized a post instance
        """

        # Uses the token passed in the `Authorization` header
        owegouser = Owegouser.objects.get(user=request.auth.user)
        bill = Bill.objects.get(pk=request.data["billId"])
        #category = Category.objects.get(pk=request.data["categoryId"])
        # Create a new Python instance of the Post class
        # and set its properties from what was sent in the
        # body of the request from the client.
        note = Note()
        note.owegouser = owegouser
        note.text = request.data["text"]
        note.date = request.data["date"]
        note.bill = bill
    

        try:
            note.save()
            serializer = NoteSerializer(note, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
       
    def update(self, request, pk=None):
        """Handle PUT requests for a note

        Returns:
            Response -- Empty body with 204 status code
        """
        owegouser = Owegouser.objects.get(user=request.auth.user)
        tag = Tag.objects.get(pk=request.data["tagId"])
        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Post, get the game record
        # from the database whose primary key is `pk`
        note = Note.objects.get(pk=pk)
        note.tag = tag
        note.owegouser = owegouser
        note.text = request.data["text"]
        note.date = request.data["date"]
        note.save()
        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single note

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            note = Note.objects.get(pk=pk)
            note.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Note.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class NoteSerializer(serializers.ModelSerializer):
    """JSON serializer for posts

    Arguments:
        serializer type
    """
    class Meta:
        model = Note
        fields = ('id', 'text', 'date')
        depth = 1
        
class NoteUserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
class NoteOwegoUserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer"""
    user = NoteUserSerializer(many=False)

    class Meta:
        model = Owegouser
        fields = ['user']
