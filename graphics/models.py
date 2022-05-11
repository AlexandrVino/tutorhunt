from django.db import models
from django.urls import reverse
from django.conf import settings
from .fields import DayTimelineField


User = settings.AUTH_USER_MODEL

WEEKDAYS_RUS = ("понедельник", "вторник", "среда",
                "четверг", "пятница", "суббота", "воскресенье")


class TimelineModel(models.Model):
    """Модель расписания"""
    (monday,
    tuesday,
    wednesday, 
    thursday,
    friday, 
    saturday,
    sunday) = [DayTimelineField(weekday) for weekday in WEEKDAYS_RUS]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="timeline")
    
    def __str__(self) -> str:
        return "Расписание %s" % self.user

    def get_absolute_url(self):
        return reverse("detail-timeline", kwargs={"pk": self.pk})
    
    def get_days_fields(self) -> tuple:
        """Выдаёт кортеж с полями-днями недели"""
        return (self.monday,
                self.tuesday,
                self.wednesday, 
                self.thursday,
                self.friday, 
                self.saturday,
                self.sunday)

    class Meta:
        verbose_name = "расписание"
        verbose_name_plural = "расписания"
