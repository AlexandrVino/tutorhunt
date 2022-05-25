from typing import Optional, Iterable
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.safestring import mark_safe

from users.managers import AppUserManager


class Role(models.TextChoices):
    TEACHER = "Teacher"
    STUDENT = "Student"


class User(AbstractUser):
    """Модель пользователя"""
    email = models.EmailField(blank=False)
    role = models.CharField(
        max_length=8,
        choices=Role.choices,
        default=Role.STUDENT,
        verbose_name="Роль"
    )
    photo = models.ImageField(
        upload_to="uploads/users/", verbose_name="Фото",
        default="uploads/users/user_default.png"
    )
    bio = models.TextField(blank=True, verbose_name="Биография",)

    manager = AppUserManager()

    def photo_tmb(self):
        """
        :return: Возвращает фото 50х50
        """

        if self.photo:
            return mark_safe(f'<img src="{self.photo.url}" class="friend_photo" width="50">')
        return mark_safe('<img src="/media/uploads/users/user_default.png" class="friend_photo">')

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"user_id": self.pk})

    def get_photo(self):
        """
        :return: Возвращает фото размера без изменений
        """

        if self.photo:
            return mark_safe(f'<img src="{self.photo.url}" class="avatar">')
        return mark_safe('<img src="/media/uploads/users/user_default.png" class="avatar">')

    def has_timeline(self):
        """
        :return: Проверяет наличие графика
        """

        return hasattr(self, "timeline")

    def full_clean(self, exclude: Optional[Iterable[str]] = None,
                   *args, **kwargs) -> None:
        super().full_clean(exclude, *args, **kwargs)

        exclude = exclude or list()

        if "first_name" not in exclude and not self.first_name:
            raise ValidationError("Имя должно быть заполнено")
        elif "last_name" not in exclude and not self.last_name:
            raise ValidationError("Фамилия должна быть заполнено")
