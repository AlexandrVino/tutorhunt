from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL


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
