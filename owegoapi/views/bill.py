"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from owegoapi.models import Bill, Category, Owegouser, Tag
from django.contrib.auth import get_user_model
User = get_user_model()

class BillView(ViewSet):
    """Bill posts"""

    def list(self, request):
        """Handle GET requests to bills resource

        Returns:
            Response -- JSON serialized list of bills
        """
        # Get all bill records from the database
        bills = Bill.objects.all()

        # Support filtering bills by type
        #    http://localhost:8000/bills?type=1
        #
        # That URL will retrieve all tabletop games
        bill_type = self.request.query_params.get('type', None)
        if bill_type is not None:
            bills = bills.filter(bill_type__id=bill_type)

        serializer = BillSerializer(
            bills, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single bill

        Returns:
            Response -- JSON serialized post instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/bills/2
            #
            # The `2` at the end of the route becomes `pk`
            bill = Bill.objects.get(pk=pk)
            serializer = BillSerializer(bill, context={'request': request})
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
        category = Category.objects.get(pk=request.data["categoryId"])
        # Create a new Python instance of the Post class
        # and set its properties from what was sent in the
        # body of the request from the client.
        bill = Bill()
        bill.owegouser = owegouser
        bill.title = request.data["title"]
        bill.category = category
        bill.due_date = request.data["dueDate"]
        bill.amount_due = request.data["amountDue"]
        bill.paid = request.data["paid"]
        bill_tag = Tag.objects.get(pk=request.data["billTagId"])
        
        try:
            bill.save()
            bill.bill_tag.add(bill_tag)
            serializer = BillSerializer(bill, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
       
   
    def update(self, request, pk=None):
        """Handle PUT requests for a bill

        Returns:
            Response -- Empty body with 204 status code
        """
        owegouser = Owegouser.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Game, get the game record
        # from the database whose primary key is `pk`
        bill = Bill.objects.get(pk=pk)
        bill.owegouser = owegouser
        bill.title = request.data["title"]
        bill.due_date = request.data["dueDate"]
        bill.amount_due = request.data["amountDue"]
        bill.paid = request.data["paid"]
        
        category = Category.objects.get(pk=request.data["categoryId"])
        bill.category = category
        bill.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single bill

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            bill = Bill.objects.get(pk=pk)
            bill.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Bill.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'label')
        
class BillTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=False)
    class Meta:
        model = Tag
        fields = ('id', 'tag')
   
class BillSerializer(serializers.ModelSerializer):
     bill_tag = BillTagSerializer(many=True)
     class Meta:
        model = Bill
        fields = ('id','title', 'due_date', 'amount_due',
                  'category', 'owegouser', 'paid', 'bill_tag','notes')
        depth = 1
        
class BillUserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
        
class BillOwegoUserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer"""
    user = BillUserSerializer(many=False)

    class Meta:
        model = Owegouser
        fields = ['user']