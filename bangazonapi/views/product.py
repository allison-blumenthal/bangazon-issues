from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import Product


class ProductView(ViewSet):
  """Bangazon API product view"""
  
  def retrieve(self, request, pk):
    """Handle GET requests for a single product
    
    Returns:
        Response -- JSON serialized product
    """
    try:
      product = Product.objects.get(pk=pk)
      
      serializer = ProductSerializer(product)
      return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Product.DoesNotExist as ex:
        return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
      
  def list(self, request):
    """Handle GET requests to get all products
    
    Returns:
        Response -- JSON serialized list of all products
    """
    
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


class ProductSerializer(serializers.ModelSerializer):
  """JSON serializer for products"""
  
  class Meta:
      model = Product
      fields = ('id', 'seller_id', 'name', 'description', 'price', 'quantity', 'product_image_url', 'added_on', 'category_id')
