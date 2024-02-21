from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, Payment
from users.permissions import UserPermission
from users.serliazers import UserSerializer, PaymentSerializer, UserLimitedSerializer, UserCreateSerializer


class UserCreateAPIView(generics.CreateAPIView):
    '''CREATE User'''
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]



class UserListAPIView(generics.ListAPIView):
    '''READ ALL User'''
    serializer_class = UserLimitedSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
     '''READ ONE User'''
     serializer_class = UserSerializer
     queryset = User.objects.all()
     permission_classes = [IsAuthenticated, UserPermission]


class UserUpdateAPIView(generics.UpdateAPIView):
    '''UPDATE PUT AND PATCH User'''
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, UserPermission]


class UserDestroyAPIView(generics.DestroyAPIView):
    '''DELETE User'''
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, UserPermission]


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Здесь ваш код для получения истории платежей пользователя
        return Response({'message': 'История платежей пользователя'})


class TokenObtainPairView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=400)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
