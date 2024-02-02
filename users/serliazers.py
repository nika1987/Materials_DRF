from rest_framework import serializers

from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'payment_amount', 'payment_date', 'stripe_id']

class UserSerializer(serializers.ModelSerializer):
    '''Расширение сериализатора для вывода истории платежей user'''
    payments = PaymentSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'



