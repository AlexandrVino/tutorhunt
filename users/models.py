from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.safestring import mark_safe

from users.managers import AppUserManager, BunchManager, FollowManager


class Role(models.TextChoices):
    TEACHER = "Teacher"
    STUDENT = "Student"


class BunchStatus(models.TextChoices):
    WAITING = "Waiting"
    ACCEPTED = "Accepted"
    FINISHED = "Finished"


class User(AbstractUser):
    email = models.EmailField(blank=False)
    role = models.CharField(
        max_length=7,
        choices=Role.choices,
        default=Role.STUDENT,
        verbose_name="Роль"
    )
    photo = models.ImageField(
        upload_to="uploads/users/", verbose_name="Фото",
        default="uploads/users/user_default.png"
    )

    manager = AppUserManager()

    def photo_tmb(self):
        if self.photo:
            return mark_safe(f'<img src="{self.photo.url}" class="friend_photo" width="50">')
        return mark_safe('<img src="/media/uploads/users/user_default.png" class="friend_photo">')

    def get_photo(self):
        if self.photo:
            return mark_safe(f'<img src="{self.photo.url}" class="avatar">')
        return mark_safe('<img src="/media/uploads/users/user_default.png" class="avatar">')

    def has_timeline(self):
        return hasattr(self, "timeline")


class Bunch(models.Model):
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
