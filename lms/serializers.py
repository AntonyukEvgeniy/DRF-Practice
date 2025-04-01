from rest_framework import serializers

from .models import Course, Lesson, Subscription
from .services.stripe_service import StripeService
from .validators import YouTubeURLValidator


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[YouTubeURLValidator("video_url")])

    class Meta:
        model = Lesson
        fields = ["id", "course", "title", "description", "preview", "video_url"]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ["id", "title", "preview", "description", "lessons_count", "lessons"]

    def get_lessons_count(self, obj):
        return obj.lessons.count()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["id", "user", "course", "created_at", "is_active"]
        read_only_fields = ["user", "created_at", "created_at"]


class CourseWithPriceSerializer(CourseSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)
    currency = serializers.CharField(max_length=3, write_only=True, default='usd')

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['price', 'currency']

    def create(self, validated_data):
        price_amount = validated_data.pop('price')
        currency = validated_data.pop('currency', 'usd')

        # Создаем курс
        course = super().create(validated_data)

        # Создаем продукт и цену в Stripe
        stripe_service = StripeService()
        product = stripe_service.create_product(
            name=course.title,
            description=course.description
        )

        # Конвертируем цену в центы для Stripe
        price_in_cents = int(price_amount * 100)
        price = stripe_service.create_price(
            product_id=product['id'],
            unit_amount=price_in_cents,
            currency=currency
        )

        # Сохраняем stripe_price_id в модели курса
        course.stripe_price_id = price['id']
        course.save()
        return course