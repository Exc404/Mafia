from celery import shared_task
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone


@shared_task
def delete_inactive_accounts(user_id):
    try:
        user = User.objects.get(pk=user_id)
        # Проверяем, активирован ли аккаунт
        if not user.is_active:
            # Удаление неактивированного аккаунта
            user.delete()
    except Exception:
        pass
