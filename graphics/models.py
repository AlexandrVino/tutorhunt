from typing import Any, Dict, Tuple

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.urls import reverse

from bunch.models import Bunch
from users.models import Role
from .fields import DayTimeline, DayTimelineField
from .utils import CONST

User = get_user_model()


class TimelineModel(models.Model):
    """Модель расписания"""
    monday, tuesday, wednesday, thursday, friday, saturday, sunday = [
      DayTimelineField(weekday, default=DayTimeline([False] * 24)) for weekday in CONST.WEEKDAYS_RUS]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="timeline")

    def __str__(self) -> str:
        return "Расписание %s" % self.user

    def get_absolute_url(self):
        return reverse("detail-timeline", kwargs={"pk": self.pk})

    def get_days_fields(self) -> tuple:
        """Выдаёт кортеж с полями-днями недели"""
        return (
            self.monday, self.tuesday, self.wednesday, self.thursday,
            self.friday, self.saturday, self.sunday
        )

    def get_table_data(self) -> Dict[str, Any]:
        """Возвращает данные для таблицы (для шаблонов)"""
        data = [[{
            "value": CONST.HOURS[j],
            "class": "busy-hour" if weekday.is_busy(j) else "vacant-hour"
        } for i, weekday in enumerate(self.get_days_fields())] for j in range(24)]

        return {"headers": CONST.WEEKDAYS_RUS, "data": data}

    def get_small_table_data(self) -> Dict[str, Tuple[str]]:
        """Возвращет данные для малой таблицы (для шаблонов)"""
        data = []
        bunches = Bunch.manager.get_objects_with_filter(teacher=self.user).order_by("datetime")

        for index, (caption, field) in enumerate(zip(CONST.WEEKDAYS_RUS, self.get_days_fields())):

            curr_line_bunches = [None] * 24
            indexes = list(filter(lambda x: x.datetime[0] == str(index + 1), bunches))
            for bunch in indexes:
                curr_line_bunches[int(bunch.datetime.split(":")[-1])] = bunch

            data.append({"caption": caption, "weekday": zip(field.timeline, CONST.HOURS, curr_line_bunches)})

        return {"hours": CONST.HOURS, "data": data}

    class Meta:
        verbose_name = "расписание"
        verbose_name_plural = "расписания"


@receiver(models.signals.post_save, sender=User)
def save_user_handler(sender, instance, *args, **kwargs):
    if not instance.has_timeline() and instance.role == Role.TEACHER:
        timeline = TimelineModel(user=instance)
        timeline.save()
