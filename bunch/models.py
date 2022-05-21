from django.contrib.auth import get_user_model
from django.db import models

from bunch.managers import BunchManager

User = get_user_model()


class BunchStatus(models.TextChoices):
    """
    Класс для хранения чойсов для связи (занятия)
    """

    WAITING = "Waiting"
    ACCEPTED = "Accepted"
    FINISHED = "Finished"


class Bunch(models.Model):
    """
    Класс модели связи (занятия)
    """

    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bunch_teacher", verbose_name="Учитель"
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bunch_student", verbose_name="Ученик"
    )
    status = models.CharField(
        max_length=16,
        default=BunchStatus.WAITING,
        choices=BunchStatus.choices,
        verbose_name="Статус",
        help_text="Поставьте стстус",
    )
    datetime = models.CharField("Время занятия", max_length=10, default=None)

    manager = BunchManager()

    def __eq__(self, other) -> bool:
        if type(other) is not type(self):
            return False
        return (
                self.teacher == other.teacher and self.student == other.student and self.datetime == other.datetime
        )

    class Meta:
        ordering = ("datetime",)
        verbose_name = "Связка"
        verbose_name_plural = "Связки"

        constraints = [models.UniqueConstraint(
            fields=["teacher", "student", "datetime"],
            name="unique_bunch",
        )]
