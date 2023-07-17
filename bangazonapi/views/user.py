from django.http import HttpResponseServerError
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazonapi.models import User
from rest_framework.views import APIView


class UserView(APIView):
  
  def get(self, request):
    """Gets all users
    
    Returns 
      Response -- single JSON serialized of users
    """
    uid = request.query_params.get('uid')
    users = User.objects.all()
    
    if uid:
        users = users.filter(uid=uid)
    
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
      

class UserSerializer(serializers.ModelSerializer):
      """JSON serializer for rare_users"""
      
      class Meta:
        model = User
        fields = ('uid', 'first_name', 'last_name', 'email', 'username', 'profile_image_url', 'registered_on', 'is_active')
          
    
