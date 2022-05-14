from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import send_notification

from users.models import Follow


@receiver(post_save, sender=Follow)
def notificate_follow(sender, instance: Follow, created, **kwargs):    
    if instance.active:
        message = f"На вас подписался {instance.user_from}"
    else:
        message = f"От вас отписался {instance.user_from}"   
     
    send_notification(
        recipient=instance.user_to,
        initiator=instance.user_from,
        category="подписки",
        message=f"На вас подписался {instance.user_from}"
    )
