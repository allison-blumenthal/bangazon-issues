from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import Order


class OrderView(ViewSet):
  """Bangazon API order view"""
  
  def retrieve(self, request, pk):
    """Handle GET requests for a single order
    
    Returns:
        Response -- JSON serialized order
    """
    try:
      order = Order.objects.get(pk=pk)
      
      serializer = OrderSerializer(order)
      return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Order.DoesNotExist as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
      
  def list(self, request):
    """Handle GET requests to get all orders
    
    Returns:
        Response -- JSON serialized list of all orders
    """
    
    orders = Order.objects.all()
    
    # filter orders by customer_id 
    customer_id = request.query_params.get('customer_id', None)
    
    if customer_id is not None:
      try:
          # customer_id query param is converted to an integer
          customer_id = int(customer_id)
      except ValueError:
          return Response({'message': 'Invalid customer_id'}, status=status.HTTP_400_BAD_REQUEST)
    #filter orders by both the customer_id and is_completed=true
    orders = Order.objects.filter(customer_id=customer_id, is_completed=True)

    
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


class OrderSerializer(serializers.ModelSerializer):
  """JSON serializer for orders"""
  
  class Meta:
      model = Order
      fields = ('id', 'customer_id', 'payment_type', 'total', 'needs_shipping', 'is_completed', 'date_placed')
      depth = 0
