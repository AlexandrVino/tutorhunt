from typing import Optional
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class NotificationModel(models.Model):
    category = models.CharField("категория", max_length=20)
    message = models.TextField("сообщение")
    read = models.BooleanField("прочитано", default=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_notifications")
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="caused_notifications",
                                  blank=True, null=True, default=None)
    creation = models.DateTimeField("дата получения", auto_now_add=True)

    class Meta:
        verbose_name = "уведомление"
        verbose_name_plural = "уведомления"


def send_notification(recipient: User, category: str,
                      message: str, initiator: Optional[User] = None) -> NotificationModel:
    """
    Создаёт уведомление (в т. ч. в db) и возвращает созданный объект
    
    Параметры:
    recipient -- получатель
    category -- категория уведомления
    message -- сообщение
    initiator (необязательно) -- отправитель

    Исключения:
    TypeError -- несоответствие типам, упомянутым в сигнатуре
    """
    for name, obj, cls in zip(("recipient", "category", "message"),
                              (recipient, category, message),
                              (User, str, str)):
        if not isinstance(obj, cls):
            raise TypeError(f"{name} должен иметь тип {cls.__name__}")

    if initiator is not None and not isinstance(initiator, User):
        raise TypeError("initiator должен иметь тип User")

    obj = NotificationModel(recipient=recipient, category=category,
                            message=message, initiator=initiator)
    obj.save()

    return obj
