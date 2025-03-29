from rest_framework import serializers

from .models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "preview", "description"]


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "course", "title", "description", "preview", "video_url"]
