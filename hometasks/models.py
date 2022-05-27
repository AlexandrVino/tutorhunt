from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import UniqueConstraint

from .managers import HometaskManager, AssignmentManager

User = get_user_model()


class Hometask(models.Model):
    title = models.CharField(max_length=50, verbose_name="Задание")
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Учитель",
        related_name="teacher_hometask",
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=False,
        help_text="Введите текст домашнего задания",
    )
    files = models.FileField(
        upload_to="uploads/hometasks", null=True, verbose_name="Файл"
    )

    manager = HometaskManager()

    def get_file_name(self):
        temp = str(self.files)
        return temp[temp.rfind("/") + 1:]

    class Meta:
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"


class Assignment(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Ученик",
        related_name="student_hometask",
    )
    hometask = models.ForeignKey(
        Hometask,
        on_delete=models.CASCADE,
        verbose_name="Домашнее задание",
        related_name="hometask",
    )
    is_completed = models.BooleanField(default=False, verbose_name="Выполнено")

    manager = AssignmentManager()

    class Meta:
        verbose_name = "Назначение"
        verbose_name_plural = "Назначения"
        constraints = [
            UniqueConstraint(
                fields=[
                    "student",
                    "hometask",
                ],
                name="unique_assignment",
            )
        ]
