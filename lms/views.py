from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsOwnerOrModerator, ModeratorPermission

from .models import Course, Lesson, Subscription
from .paginators import StandardResultsSetPagination
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer


# ViewSet для модели Course
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]
    pagination_class = StandardResultsSetPagination
    def get_queryset(self):
        if self.request.user.groups.filter(name="moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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
        course_id = self.kwargs.get('course_id')
        user = self.request.user
        subscription = Subscription.objects.filter(
            user=user,
            course_id=course_id
        ).first()
        if not subscription:
            subscription = Subscription.objects.create(
                user=user,
                course_id=course_id,
                is_active=False
            )
        return subscription
