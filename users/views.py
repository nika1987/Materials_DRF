from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User, Payment
from users.serliazers import UserSerializer, PaymentSerializer


class UserCreateAPIView(generics.CreateAPIView):
    '''CREATE User'''
    serializer_class = UserSerializer


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Здесь ваш код для получения истории платежей пользователя
        return Response({'message': 'История платежей пользователя'})
