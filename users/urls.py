from django.urls import path, include
from rest_framework.routers import DefaultRouter


from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserProfileView

app_name = UsersConfig.name

urlpatterns = [
    path('create_user/', UserCreateAPIView.as_view(), name='user-create'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),

]
