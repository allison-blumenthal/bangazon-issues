from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import Product, User, Category


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
  
  def create(self, request):
      """Handle POST operations for products
      
      Returns:
          Response -- JSON serialized product instance
      """
      
      seller_id = User.objects.get(pk=request.data["sellerId"])
      category_id = Category.objects.get(pk=request.data["categoryId"])
      
      product = Product.objects.create(
        seller_id=seller_id,
        category_id=category_id,
        name=request.data["name"],
        description=request.data["description"],
        price=request.data["price"],
        quantity=request.data["quantity"],
        product_image_url=request.data["productImageUrl"],
        added_on=request.data["addedOn"]
      )
      serializer = ProductSerializer(product)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
  def destroy(self, request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)  


class ProductSerializer(serializers.ModelSerializer):
  """JSON serializer for products"""
  
  class Meta:
      model = Product
      fields = ('id', 'seller_id', 'name', 'description', 'price', 'quantity', 'product_image_url', 'added_on', 'category_id')
