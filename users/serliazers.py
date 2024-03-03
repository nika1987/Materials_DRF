from django.contrib.auth.hashers import make_password
from django.forms import forms
from rest_framework import serializers

from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def get_payment_stripe(self, instance):

        request = self.context.get('request')

        if request.stream.method == 'POST':
            stripe_id = create_payment(int(instance.payment_amount))
            obj_payments = Payment.objects.get(id=instance.id)
            obj_payments.stripe_id = stripe_id
            obj_payments.save()
            return retrieve_payment(stripe_id)
        if request.stream.method == 'GET':
            if not instance.stripe_id:
                return None
            return retrieve_payment(instance.stripe_id)


class UserCreateSerializer(serializers.ModelSerializer):
    '''Создание пользователя'''

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super(UserCreateSerializer, self).create(validated_data)


    class Meta:
        model = User
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    '''Расширение сериализатора для вывода истории платежей user'''
    payments = PaymentSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        '''Скрыть пароль в профиле'''
        super().__init__(*args, **kwargs)
        #self.fields['password'].required = False


class UserLimitedSerializer(serializers.ModelSerializer):
    '''Исключает отображение пароля и фамилии'''

    class Meta:
        model = User
        exclude = ('password', 'last_name')

