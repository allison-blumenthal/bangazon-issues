from django.http import HttpResponseServerError
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import User
from rest_framework.views import APIView


class UserView(APIView):
  
  # the get method below is replacing the list method 
  # and inheriting from APIView
  def get(self, request):
    """Gets all users
    
    Returns 
      Response -- JSON serialized list of users
    """
    
    # get all users 
    users = User.objects.all()
    
    # Establish the query parameter of uid and 
    # use the .get method to retrieve the object with matching 
    # uid value. If no user is found, an exception is raised.
    uid = request.query_params.get('uid')
    
    # if the uid exists, filter the list of users by the uid
    if uid:
        users = users.filter(uid=uid)
    
    # serialize any matching instances
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
      

class UserSerializer(serializers.ModelSerializer):
      """JSON serializer for rare_users"""
      
      class Meta:
        model = User
        fields = ('id', 'uid', 'first_name', 'last_name', 'email', 'username', 'profile_image_url', 'registered_on', 'is_active')
          
    
