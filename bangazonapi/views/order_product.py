"""View module for handling requests about song genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import Order, Product, OrderProduct


class OrderProductView(ViewSet):
    """Bangazon API order_product view"""
    
    def retrieve(self, request, pk):
      """Handle GET requests for a single order_prodcut
      
      Returns:
          Response -- JSON serialized order_product
      """
      
      try:
          order_product = OrderProduct.objects.get(pk=pk)
          
          serializer = OrderProductSerializer(order_product)
          return Response(serializer.data, status=status.HTTP_200_OK)
        
      except OrderProduct.DoesNotExist as ex:
          return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        
    def list(self, request):
      """Handle GET requests to get all order_prodcuts
    
      Returns:
          Response -- JSON serialized list of all order_products
      """
    
      order_products = OrderProduct.objects.all()
      
      # filter to query orders_products by order_id
      order_id = request.query_params.get('order_id', None)
      
      if order_id is not None:
        order_products = order_products.filter(order_id_id=order_id)
      
      serializer = OrderProductSerializer(order_products, many=True)
      return Response(serializer.data)
  
    def create(self, request):
        """Handle POST operations for order_product
        
        Returns
            Response -- JSON serialized order_product instance
        """
        
        order_id = Order.objects.get(pk=request.data["orderId"])
        product_id = Product.objects.get(pk=request.data["productId"])
        
        order_product = OrderProduct.objects.create(
            order_id=order_id,
            product_id=product_id,
            quantity=request.data["quantity"]
        )
        serializer = OrderProductSerializer(order_product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderProductSerializer(serializers.ModelSerializer):
  """JSON serializer for order_products"""

  class Meta:
      model = OrderProduct
      fields = ('id', 'order_id', 'product_id', 'quantity')
      depth = 0
