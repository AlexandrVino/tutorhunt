from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.safestring import mark_safe

from users.managers import AppUserManager, BunchManager, FollowManager


class Role(models.TextChoices):
    TEACHER = 'Teacher'
    STUDENT = 'Student'

# form-control input-field role

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
        default='uploads/users/user_default.png'
    )

    manager = AppUserManager()

    def photo_tmb(self):
        if self.photo:
            return mark_safe(f'<img src="{self.photo.url}" class="friend_photo" width="50">')
        return mark_safe(f'<img src="/media/uploads/users/user_default.png" class="friend_photo">')

    def get_photo(self):
        if self.photo:
            return mark_safe(f'<img src="{self.photo.url}" class="avatar">')
        return mark_safe(f'<img src="/media/uploads/users/user_default.png" class="avatar">')


class Bunch(models.Model):
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bunch_teacher', verbose_name='Учитель'
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bunch_student', verbose_name='Ученик'
    )

    status = models.SmallIntegerField(
        blank=True, default=1,
        choices=(
            (1, "waiting"), (2, "accepted"), (3, "finished")
        ),
        help_text="Поставьте стстус",
    )

    manager = BunchManager()

    class Meta:
        verbose_name = 'Связка'
        verbose_name_plural = 'Связки'

        constraints = [models.UniqueConstraint(
            fields=["teacher", "student"],
            name="unique_bunch",
        )]


class Follow(models.Model):
    user_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follow_from', verbose_name='Подписчик')
    user_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follow_to', verbose_name='Человек, на которого подписываются')
    active = models.BooleanField(default=True)

    manager = FollowManager()

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

        constraints = [models.UniqueConstraint(fields=["user_to", "user_from"], name="unique_follow")]
