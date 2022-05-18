from typing import Any, Dict
from django.http import HttpRequest
from django.contrib.auth import get_user_model

from notifications.models import NotificationModel, NotificationQueryset

User = get_user_model()


def add_notifications(request: HttpRequest) -> Dict[str, Any]:
    """Контекст-процессор для добавления уведомлений"""
    if not request.user.is_authenticated:
        return {}

    notifications: NotificationQueryset = NotificationModel.objects.by_recipient(request.user)
    return {"notifications": notifications, "has_unread_notifications": bool(notifications.get_unread())}
