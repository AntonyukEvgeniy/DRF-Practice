import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from lms.models import Course, Lesson
from users.models import Payment

User = get_user_model()
fake = Faker("ru_RU")


class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми данными"

    def handle(self, *args, **options):
        # Создаем пользователей
        self.stdout.write("Создание пользователей...")
        users = []
        for _ in range(10):
            email = fake.email()
            user = User.objects.create_user(
                email=email,
                password="testpass123",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=fake.phone_number(),
                city=fake.city(),
            )
            self.stdout.write(self.style.SUCCESS(f"Created user with email: {email}"))
            users.append(user)
        # Создаем курсы
        self.stdout.write("Создание курсов...")
        courses_data = [
            {
                "title": "Python для начинающих",
                "description": fake.text(1000),
                "lessons_count": 15,
            },
            {
                "title": "Python Developer Pro",
                "description": fake.text(1000),
                "lessons_count": 45,
            },
            {
                "title": "Go developer",
                "description": fake.text(1000),
                "lessons_count": 55,
            },
        ]
        courses = []
        for course_data in courses_data:
            course = Course.objects.create(
                title=course_data["title"], description=course_data["description"]
            )
            courses.append(course)
            # Создаем уроки для курса
            self.stdout.write(f"Создание уроков для курса {course.title}...")
            for lesson_num in range(course_data["lessons_count"]):
                Lesson.objects.create(
                    course=course,
                    title=f"Урок {lesson_num + 1}: {fake.sentence()}",
                    description=fake.text(500),
                    video_url=f"https://example.com/video/{fake.uuid4()}",
                )
                # Создаем тестовые платежи
                self.stdout.write("Создание тестовых платежей...")
                payment_methods = ["cash", "transfer", "card"]

                # Создаем платежи для курсов
                for user in users:
                    for course in courses:
                        if random.choice([True, False]):  # Случайный выбор оплаты
                            Payment.objects.create(
                                user=user,
                                paid_course=course,
                                amount=random.uniform(1000.00, 5000.00),
                                payment_method=random.choice(payment_methods),
                            )
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"Created payment for course {course.title} by user {user.email}"
                                )
                            )

                self.stdout.write(
                    self.style.SUCCESS("Тестовые данные успешно созданы!")
                )
        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно созданы!"))
        self.stdout.write("Создано:")
        self.stdout.write(f"- Пользователей: {len(users)}")
        self.stdout.write(f"- Курсов: {len(courses)}")
        self.stdout.write(f"- Уроков: {Lesson.objects.count()}")
