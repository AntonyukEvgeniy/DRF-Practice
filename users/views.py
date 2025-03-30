from django_filters import FilterSet, DateFilter, NumberFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import AllowAny

from .models import User, Payment
from .serializers import UserProfileSerializer, UserRegistrationSerializer, PaymentSerializer


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]


class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer


class PaymentFilter(FilterSet):
    payment_date_from = DateFilter(field_name='payment_date', lookup_expr='gte')
    payment_date_to = DateFilter(field_name='payment_date', lookup_expr='lte')
    amount_min = NumberFilter(field_name='amount', lookup_expr='gte')
    amount_max = NumberFilter(field_name='amount', lookup_expr='lte')
    class Meta:
        model = Payment
        fields = ['payment_method', 'paid_course', 'paid_lesson', 'user']


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']  # По умолчанию сортировка по убыванию даты