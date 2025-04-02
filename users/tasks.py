from celery import shared_task
from celery.utils.log import get_logger
from django.utils import timezone
from .models import User
from dateutil.relativedelta import relativedelta

logger = get_logger(__name__)


@shared_task
def deactivate_inactive_users():
    """
    Проверяет пользователей, которые не входили в систему более месяца,
    и деактивирует их аккаунты.
    """
    # Вычисляем дату месяц назад от текущей даты
    month_ago = timezone.now() - relativedelta(months=1)

    # Находим и деактивируем неактивных пользователей
    inactive_users = User.objects.filter(last_login__lt=month_ago, is_active=True)
    count = inactive_users.update(is_active=False)
    logger.info(f"Деактивировано {count} неактивных пользователей")
