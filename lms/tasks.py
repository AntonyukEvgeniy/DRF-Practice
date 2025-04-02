from datetime import timedelta

from celery import shared_task
from celery.utils.log import get_logger
from django.core.mail import send_mail
from django.utils import timezone
from environs import env

from lms.models import Course, Subscription

logger = get_logger(__name__)


@shared_task
def send_course_update_notification(course_id):
    """
    Отправляет письмо на email всем подписчикам курса, по событию обновления курса
    """
    course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(course=course, is_active=True)
    # Проверяем, прошло ли 4 часа с последнего обновления
    four_hours_ago = timezone.now() - timedelta(hours=4)
    if course.last_update and course.last_update > four_hours_ago:
        logger.info("Уведомление не отправлено: курс обновлялся менее 4 часов назад")
    for subscription in subscriptions:
        send_mail(
            subject=f'Курс "{course.title}" был обновлен',
            message=f'Здравствуйте! Курс "{course.title}" был обновлен.\nПроверьте новое содержание курса.',
            from_email=env.str("EMAIL_HOST_USER"),
            recipient_list=[subscription.user.email],
            fail_silently=False,
        )
    logger.info("Все уведомления успешно отправлены")
