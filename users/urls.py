from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("profile/<int:pk>/", views.UserProfileUpdateView.as_view(), name="profile"),
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("payments/", views.PaymentListView.as_view(), name="payment-list"),
]
