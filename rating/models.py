from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint

from .managers import RatingManager


User = get_user_model()


class Rating(models.Model):
    choices = (
        ("0", "-"),
        ("1", "*"),
        ("2", "**"),
        ("3", "***"),
        ("4", "****"),
        ("5", "*****"),
    )
    star = models.CharField(
        verbose_name="Оценка", default=0, max_length=1, choices=choices
    )

    user_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="rating_to",
        verbose_name="Получатель",
    )
    user_from = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="rating_from",
        verbose_name="Отправитель",
    )

    manager = RatingManager()

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        constraints = [
            UniqueConstraint(
                fields=[
                    "user_to",
                    "user_from",
                ],
                name="unique_rating",
            )
        ]

    def __str__(self):
        return str(self.star)
