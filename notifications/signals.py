import datetime as dt
from typing import Optional, Tuple

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone

from bunch.models import Bunch, BunchStatus
from chats.models import Message
from follow.models import Follow
from notifications.models import NotificationModel, send_notification
from rating.models import Rating

User = get_user_model()

# Допустимая разница между уведомлениями
ALLOWABLE_DELTA_FOR_CHATS = dt.timedelta(hours=2)
ALLOWABLE_DELTA_FOR_FOLLOW = dt.timedelta(days=1)


def check_allowable_delta(
    allowable_delta: dt.timedelta, **kwargs
) -> Tuple[bool, Optional[NotificationModel]]:
    """
    Проверяет, необходимо ли добавить новое уведомление
    Параметры:
        allowable_delta: минимальное время между уведомлениями
        **kwargs: параметры для NotificationModel.objects.filter_by
    Возвращает:
        bool (прошло ли необходимое время)
        NotificationModel (последнее уведомление) или None (если такого нет)
    """
    last_notification: Optional[NotificationModel] = (
        NotificationModel.objects.filter_by(**kwargs).order_by("last_modified").last()
    )

    if last_notification is not None:
        delta: dt.timedelta = timezone.now() - last_notification.last_modified
        return delta >= allowable_delta, last_notification
    return True, None


@receiver(post_save, sender=Follow)
def notify_follow(sender, instance: Follow, **kwargs):
    notification_kwargs = {
        "category": "подписки",
        "initiator": instance.user_from,
        "recipient": instance.user_to,
    }
    if instance.active:
        message = f"На вас подписался {instance.user_from}"
    else:
        message = f"От вас отписался {instance.user_from}"

    need_send, last_notification = check_allowable_delta(
        ALLOWABLE_DELTA_FOR_FOLLOW, **notification_kwargs
    )

    if not need_send:
        last_notification.message = message
        last_notification.save()
    else:
        send_notification(message=message, **notification_kwargs)


@receiver(post_save, sender=Rating)
def notify_rating(sender, instance: Rating, **kwargs):
    if instance.star != 0:
        send_notification(
            recipient=instance.user_to,
            initiator=instance.user_from,
            category="рейтинг",
            message="Вам выставлена оценка: %s" % instance.star,
        )


@receiver(post_save, sender=Bunch)
def notify_bunch(sender, instance: Bunch, **kwargs):
    if instance.status != BunchStatus.FINISHED:
        notification_kwargs = {
            BunchStatus.ACCEPTED: {
                "message": "Ваша заявка для %s принята" % instance.teacher,
                "category": "уроки",
                "initiator": instance.teacher,
                "recipient": instance.student,
            },
            BunchStatus.WAITING: {
                "message": "Вам пришла заявка на урок от %s" % instance.student,
                "category": "уроки",
                "initiator": instance.student,
                "recipient": instance.teacher,
            },
        }[instance.status]

        send_notification(**notification_kwargs)


@receiver(post_save, sender=Message)
def notify_message(sender, instance: Message, created: bool, **kwargs):
    if not created:
        return

    notification_kwargs = {
        "recipient": instance.get_recipient(),
        "initiator": instance.owner,
        "category": "чаты",
    }

    need_send = check_allowable_delta(ALLOWABLE_DELTA_FOR_CHATS, **notification_kwargs)[0]

    if need_send:
        send_notification(
            message="Вам отправлено сообщение(я) от %s" % instance.owner,
            **notification_kwargs,
        )
