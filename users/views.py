from django_filters import DateFilter, FilterSet, NumberFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Payment, User
from .serializers import (
    MyTokenObtainPairSerializer,
    PaymentSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
)


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer


class UserProfileUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserProfileSerializer(user).data,
                "message": "Пользователь успешно зарегистрирован",
            },
            status=status.HTTP_201_CREATED,
        )


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active", "city"]
    search_fields = ["email", "first_name", "last_name"]
    ordering_fields = ["date_joined", "email"]
    ordering = ["-date_joined"]


class PaymentFilter(FilterSet):
    payment_date_from = DateFilter(field_name="payment_date", lookup_expr="gte")
    payment_date_to = DateFilter(field_name="payment_date", lookup_expr="lte")
    amount_min = NumberFilter(field_name="amount", lookup_expr="gte")
    amount_max = NumberFilter(field_name="amount", lookup_expr="lte")

    class Meta:
        model = Payment
        fields = ["payment_method", "paid_course", "paid_lesson", "user"]


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = PaymentFilter
    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]  # По умолчанию сортировка по убыванию даты
