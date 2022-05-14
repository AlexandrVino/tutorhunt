from typing import Optional
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class NotificationQueryset(models.QuerySet):
    def by_recipient(self, user: User):
        """Сортирует queryset по получателю"""
        return self.filter(recipient=user)
    
    def by_category(self, category: str):
        """Сортирует queryset по категории"""
        return self.filter(category=category)

    def by_initiator(self, initiator: User):
        """Сортирует quryset по отправителю"""
        return self.filter(initiator=initiator)

    def filter_by(self, category: str = None, initiator: User = None, recipient: User = None):
        """Сортирует уведомления по категории, отправителю и получателю (ни один аргумент необязателен)"""
        result = self.all()

        if category is not None:
            result = result.by_category(category)
        if initiator is not None:
            result = result.by_initiator(initiator)
        if recipient is not None:
            result = result.by_recipient(recipient)

        return result
    
    def get_unread(self):
        """Возвращает непрочитанные уведомления"""
        return self.filter(read=False)
    
    def get_read(self):
        """Возвращает прочитанные уведомления"""
        return self.filter(read=True)


class NotificationModel(models.Model):
    category = models.CharField("категория", max_length=20)
    message = models.TextField("сообщение")
    read = models.BooleanField("прочитано", default=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_notifications")
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="caused_notifications",
                                  blank=True, null=True, default=None)
    creation = models.DateTimeField("дата получения", auto_now_add=True)
    
    objects = NotificationQueryset.as_manager()

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
