from rest_framework import generics
from .models import Payment
from users.serliazers import PaymentSerializer
from .filters import PaymentFilter


class PaymentList(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_class = PaymentFilter
