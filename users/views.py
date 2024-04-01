
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, serializers
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from users.models import User, Payment
from users.permissions import UserPermission
from users.serliazers import UserSerializer, PaymentSerializer, UserLimitedSerializer, UserCreateSerializer
from users.services import get_session, generate_payment_id, create_stripe_session


class UserCreateAPIView(generics.CreateAPIView):
    """CREATE User"""
    serializer_class = UserCreateSerializer
    #permission_classes = [AllowAny]


class UserListAPIView(generics.ListAPIView):
    """READ ALL User"""
    serializer_class = UserLimitedSerializer
    queryset = User.objects.all()
    #permission_classes = [IsAuthenticated, UserPermission]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """READ ONE User"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, UserPermission]


class UserUpdateAPIView(generics.UpdateAPIView):
    """UPDATE PUT AND PATCH User"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, UserPermission]


class UserDestroyAPIView(generics.DestroyAPIView):
    """DELETE User"""
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, UserPermission]


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        # Здесь ваш код для получения истории платежей пользователя
        return Response({'message': 'История платежей пользователя'})


class PaymentListAPIView(generics.ListAPIView):
    """READ ALL Payments, Добавлена фильтрация"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['paid_date']
    permission_classes = [IsAuthenticated]


class PaymentCreateApiView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        course = serializer.validated_data.get('course')
        if not course:
            raise serializers.ValidationError('Course is required.')
        payment = serializer.save()
        payment.user = self.request.user
        if payment.method == 'Transfer':
            payment.payment_session = create_stripe_session(payment).id
        payment.save()
