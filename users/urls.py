from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .apps import UsersConfig
from .views import MyTokenObtainPairView

app_name = UsersConfig.name


urlpatterns = [
    path("profile/<int:pk>/", views.UserProfileUpdateView.as_view(), name="profile"),
    path("", views.UserListView.as_view(), name="users"),
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("payments/", views.PaymentListView.as_view(), name="payment-list"),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
