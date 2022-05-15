from email.policy import default
from typing import Any, Dict, Tuple
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings
from .fields import DayTimeline, DayTimelineField

User = settings.AUTH_USER_MODEL

WEEKDAYS_RUS = ("понедельник", "вторник", "среда",
                "четверг", "пятница", "суббота", "воскресенье")
HOURS = tuple(['%02d:00' % i for i in range(24)])


class TimelineModel(models.Model):
    """Модель расписания"""
    (monday,
     tuesday,
     wednesday,
     thursday,
     friday,
     saturday,
     sunday) = [DayTimelineField(weekday, default=DayTimeline([False] * 24)) for weekday in WEEKDAYS_RUS]
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
        data = [[None for __ in range(7)] for _ in range(24)]
        for i, weekday in enumerate(self.get_days_fields()):
            for j in range(24):
                data[j][i] = {
                    "value": HOURS[j],
                    "class": "busy-hour" if weekday.is_busy(j) else "vacant-hour"
                }
        return {"headers": WEEKDAYS_RUS, "data": data}

    def get_small_table_data(self) -> Dict[str, Tuple[str]]:
        """Возвращет данные для малой таблицы (для шаблонов)"""
        data = []
        for index, (caption, field) in enumerate(zip(WEEKDAYS_RUS, self.get_days_fields())):
            data.append({"caption": caption, "weekday": zip(field.timeline, HOURS)})

        return {
            "hours": HOURS,
            "data": data
        }

    class Meta:
        verbose_name = "расписание"
        verbose_name_plural = "расписания"


@receiver(models.signals.post_save, sender=User)
def save_user_handler(sender, instance, *args, **kwargs):
    if not instance.has_timeline():
        timeline = TimelineModel(user=instance)
        timeline.save()
