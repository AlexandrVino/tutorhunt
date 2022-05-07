from django.db import models
from .fields import DayTimelineField


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
    
    def __str__(self) -> str:
        return "Расписание %s" % self.id

    class Meta:
        verbose_name = "расписание"
        verbose_name_plural = "расписания"
