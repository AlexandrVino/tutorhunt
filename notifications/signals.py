from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import send_notification
from rating.models import Rating

from users.models import Bunch, BunchStatus, Follow


@receiver(post_save, sender=Follow)
def notify_follow(sender, instance: Follow, **kwargs):
    if instance.active:
        message = f"На вас подписался {instance.user_from}"
    else:
        message = f"От вас отписался {instance.user_from}"   
     
    send_notification(
        recipient=instance.user_to,
        initiator=instance.user_from,
        category="подписки",
        message=message
    )


@receiver(post_save, sender=Rating)
def notify_rating(sender, instance: Rating, **kwargs):
    if instance.star != "0":
        send_notification(
            recipient=instance.user_to,
            initiator=instance.user_from,
            category="рейтинг",
            message="Вам выставлена оценка: %s" % instance.star
        )


@receiver(post_save, sender=Bunch)
def notify_bunch(sender, instance: Bunch, **kwargs):
    if instance.status != BunchStatus.FINISHED:
        notification_kwargs = {
            BunchStatus.ACCEPTED: {
                "message": "Ваша заявка для %s принята" % instance.teacher,
                "category": "уроки",
                "initiator": instance.teacher,
                "recipient": instance.student
            },
            BunchStatus.WAITING: {
                "message": "Вам пришла заявка на урок от %s" % instance.student,
                "category": "уроки",
                "initiator": instance.student,
                "recipient": instance.teacher
            }
        }[instance.status]

        send_notification(**notification_kwargs)
