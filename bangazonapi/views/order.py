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
    customer_orders = request.query_params.get('customer_id', None)
    if customer_orders is not None:
        orders = orders.filter(customer_id=customer_orders)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


class OrderSerializer(serializers.ModelSerializer):
  """JSON serializer for orders"""
  
  class Meta:
      model = Order
      fields = ('id', 'customer_id', 'payment_type', 'total', 'needs_shipping', 'is_completed', 'date_placed')
      depth = 1
