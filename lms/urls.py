from django.urls import include, path
from rest_framework import routers

from lms.views import (
    CourseViewSet,
    LessonListCreateView,
    LessonRetrieveUpdateDestroyView, SubscriptionUpdateView,
)

app_name = "lms"
router = routers.DefaultRouter()
router.register(r"courses", CourseViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", LessonListCreateView.as_view(), name="lesson-list-create"),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveUpdateDestroyView.as_view(),
        name="lesson-detail",
    ),
path("courses/<int:course_id>/subscription/", SubscriptionUpdateView.as_view(), name="subscription-update"),
]
