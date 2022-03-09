"""View module for handling requests about games"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from owegoapi.models import Bill, Category

class BillView(ViewSet):
    """Bill posts"""

    def list(self, request):

        # Get all game records from the database
        bills = Bill.objects.all() 

        # Support filtering posts by category
        #    http://localhost:8000/bills?category=1
        #
        # That URL will retrieve all tabletop posts
        category_num = self.request.query_params.get('category', None)
        if category_num is not None:
            bills = bills.filter(category__id=category_num)

        serializer = BillSerializer(
            bills, many=True, context={'request': request})
        return Response(serializer.data)
    
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
        User = User.objects.get(user=request.auth.user)
        #category = Category.objects.get(pk=request.data["categoryId"])
        # Create a new Python instance of the Post class
        # and set its properties from what was sent in the
        # body of the request from the client.
        bill = Bill()
        bill.title = request.data["title"]
        category = request.data["category"]
        bill.note = request.data["note"]
        bill.due_date = request.data["dueDate"]
        bill.amount_due = request.data["amountDue"]
        bill.paid = False
    
        category = Category.objects.get(pk=request.data["categoryId"])
        bill.category = category

        try:
            bill.save()
            serializer = BillSerializer(bill, context={'request': request})
            return Response(serializer.data)

        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
       
   


class BillSerializer(serializers.ModelSerializer):
    """JSON serializer for posts

    Arguments:
        serializer type
    """
    class Meta:
        model = Bill
        fields = ('id', 'user', 'title', 'note', 'due_date', 'amount_due',
                  'category','paid')
        depth = 1