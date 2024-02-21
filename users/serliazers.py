from django.contrib.auth.hashers import make_password
from django.forms import forms
from rest_framework import serializers

from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'paid_date']


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

