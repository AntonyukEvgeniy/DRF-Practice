from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Course, Lesson

User = get_user_model()


class LessonCRUDTests(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            email='test@test.com',
            password='testpass123'
        )
        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

        # Создаем тестовый курс
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )

        # Создаем тестовый урок
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Test Lesson',
            description='Test Description',
            video_url='https://youtube.com/watch?v=test'
        )

        # URLs для тестирования
        self.list_create_url = reverse('lms:lesson-list-create')
        self.detail_url = reverse('lms:lesson-detail', kwargs={'pk': self.lesson.pk})

    def test_create_lesson(self):
        """Тест создания урока"""
        data = {
            'course': self.course.id,
            'title': 'New Lesson',
            'description': 'New Description',
            'video_url': 'https://youtube.com/watch?v=new'
        }
        response = self.client.post(self.list_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_list_lessons(self):
        """Тест получения списка уроков"""
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_lesson(self):
        """Тест получения конкретного урока"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Lesson')

    def test_update_lesson(self):
        """Тест обновления урока"""
        data = {
            'course': self.course.id,
            'title': 'Updated Lesson',
            'description': 'Updated Description',
            'video_url': 'https://youtube.com/watch?v=updated'
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Lesson')

    def test_delete_lesson(self):
        """Тест удаления урока"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionTests(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            email='test@test.com',
            password='testpass123'
        )
        # Аутентифицируем пользователя
        self.client.force_authenticate(user=self.user)

        # Создаем тестовый курс
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )

        # URL для тестирования подписки
        self.subscription_url = reverse('lms:subscription-update',
                                        kwargs={'course_id': self.course.id})

    def test_subscription_toggle(self):
        """Тест переключения подписки"""
        # Проверяем создание подписки
        response = self.client.patch(self.subscription_url, {'is_active': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_active'])

        # Проверяем отключение подписки
        response = self.client.patch(self.subscription_url, {'is_active': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_active'])