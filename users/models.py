from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    TEACHER = 'Teacher'
    STUDENT = 'Student'


class User(AbstractUser):
    email = models.EmailField(blank=False)
    role = models.CharField(
        max_length=7,
        choices=Role.choices,
        default=Role.STUDENT,
    )
    photo = models.ImageField(
        upload_to="uploads/users/", null=True, blank=True, verbose_name="Фото"
    )


class Bunch(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bunch_teacher')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bunch_student')

    status = models.SmallIntegerField(
        blank=True, default=1,
        choices=(
            (1, "waiting"), (2, "accepted"), (3, "finished")
        ),
        help_text="Поставьте стстус",
    )


class Follow(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_from')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_to')
