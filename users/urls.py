from django.urls import path, include
from rest_framework.routers import DefaultRouter


from users.apps import UsersConfig
from users.views import UserCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('create_user/', UserCreateAPIView.as_view(), name='user-create'),

]
