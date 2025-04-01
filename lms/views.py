from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsOwnerOrModerator
from users.tasks import send_course_update_notification

from .models import Course, Lesson, Subscription
from .paginators import StandardResultsSetPagination
from .serializers import (
    CourseSerializer,
    CourseWithPriceSerializer,
    LessonSerializer,
    SubscriptionSerializer,
)
from .services.stripe_service import StripeService


# ViewSet для модели Course
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_moderator:
            return qs
        return qs.filter(owner=self.request.user)

    def perform_update(self, serializer):
        course = serializer.save(owner=self.request.user)
        send_course_update_notification.delay(course.id)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return CourseWithPriceSerializer
        return CourseSerializer

    @action(detail=True, methods=["post"])
    def create_checkout_session(self, request, pk=None):
        """
        Создает сессию оплаты для курса
        """
        course = self.get_object()

        # Получаем или создаем цену в Stripe
        stripe_service = StripeService()

        # Создаем сессию оплаты
        success_url = request.build_absolute_uri(f"/courses/{course.id}/success/")
        cancel_url = request.build_absolute_uri(f"/courses/{course.id}/cancel/")

        session = stripe_service.create_payment_link_session(
            course_id=str(course.id),
            price_id=course.stripe_price_id,
            success_url=success_url,
            cancel_url=cancel_url,
        )

        return Response({"session_id": session["id"], "checkout_url": session["url"]})


# Generic views для модели Lesson
class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class SubscriptionUpdateView(generics.UpdateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        course_id = self.kwargs.get("course_id")
        user = self.request.user
        subscription = Subscription.objects.filter(
            user=user, course_id=course_id
        ).first()
        if not subscription:
            subscription = Subscription.objects.create(
                user=user, course_id=course_id, is_active=False
            )
        return subscription
