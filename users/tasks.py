from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from environs import env

from lms.models import Subscription

from .models import Course, User


@shared_task
def send_course_update_notification(course_id):
    """
    Отправляет письмо на email всем подписчикам курса, по событию обновления курса
    """
    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course, is_active=True)
        # Проверяем, прошло ли 4 часа с последнего обновления
        four_hours_ago = timezone.now() - timedelta(hours=4)
        if course.last_update and course.last_update > four_hours_ago:
            return "Уведомление не отправлено: курс обновлялся менее 4 часов назад"
        for subscription in subscriptions:
            send_mail(
                subject=f'Курс "{course.title}" был обновлен',
                message=f'Здравствуйте! Курс "{course.title}" был обновлен.\nПроверьте новое содержание курса.',
                from_email=env.str("EMAIL_HOST_USER"),
                recipient_list=[subscription.user.email],
                fail_silently=False,
            )
        return f"Успешно отправлены уведомления для курса: {course.title}"
    except Course.DoesNotExist:
        return f"Курс с идентификатором {course_id} не найден"


@shared_task
def deactivate_inactive_users():
    """
    Проверяет пользователей, которые не входили в систему более месяца,
    и деактивирует их аккаунты.
    """
    # Вычисляем дату месяц назад от текущей даты
    month_ago = timezone.now() - timedelta(days=30)

    # Находим и деактивируем неактивных пользователей
    inactive_users = User.objects.filter(last_login__lt=month_ago, is_active=True)
    count = inactive_users.update(is_active=False)

    return f"Деактивировано {count} неактивных пользователей"
