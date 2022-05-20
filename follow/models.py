from django.contrib.auth import get_user_model
from django.db import models

from follow.managers import FollowManager

User = get_user_model()


class Follow(models.Model):
    user_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follow_from", verbose_name="Подписчик")
    user_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follow_to", verbose_name="Человек, на которого подписываются")
    active = models.BooleanField(default=True)

    manager = FollowManager()

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

        constraints = [models.UniqueConstraint(fields=["user_to", "user_from"], name="unique_follow")]
