from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import UserProfileSerializer, UserRegistrationSerializer


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]


class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
