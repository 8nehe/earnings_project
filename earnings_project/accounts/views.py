from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serailizers import UserRegistrationSerializer
from rest_framework import status
User = get_user_model()

from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import api_view


"""
View 
- Handle  user registration
- Expect a email and password - REQUIRED
- Validate email and password
- Save the data
- Return a response to the client
"""

@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello, World!"}, status=status.HTTP_200_OK)

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Registration successfull"}, status=status.HTTP_400_BAD_REQUEST)
