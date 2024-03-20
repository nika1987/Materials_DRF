from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserProfileView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, \
    UserDestroyAPIView, PaymentListAPIView, PaymentCreateApiView

app_name = UsersConfig.name


urlpatterns = [
    path('create_user/', UserCreateAPIView.as_view(), name='user-create'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('', UserListAPIView.as_view(), name='user_list'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user_one'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user_delete'),
    # Authorise Tokens
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # PAYMENT
    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
    path('payment/create/', PaymentCreateApiView.as_view(), name='course-payment'),

]
