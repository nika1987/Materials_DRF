from rest_framework import generics

from users.models import User
from users.serliazers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    '''CREATE User'''
    serializer_class = UserSerializer
