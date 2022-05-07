from django.db import models
from django.contrib.auth import get_user_model

from .managers import HometaskManager


User = get_user_model()


class Hometask(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Ученик",
        related_name="student_hometask",
    )
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

    objects = HometaskManager()

    class Meta:
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"
