from typing import Iterable, List, Union
from django.db import models

class DayTimeline:
    """Расписание дня"""
    timeline: List[bool]

    def __init__(self, timeline: Iterable[bool] = None):
        if timeline is None:
            self.timeline = (False, ) * 24
        else:
            self.timeline = list(timeline)

        if len(self.timeline) != 24:
            raise ValueError("Количество часов должно быть равно 24")

        if any(map(lambda x: not isinstance(x, bool), self.timeline)):
            raise TypeError("В timeline могут быть только bool")

    def __str__(self) -> str:
        return str(map(lambda x: 1 if x else 0, self.timeline))

    @classmethod
    def parse_timeline(value: str) -> "DayTimeline":
        """
        Обработка строкового представления расписания. 
        
        Параметры:
        value -- строковое представление

        Возвращет соответствующий DayTimeline
        """
        return DayTimeline(timeline=tuple(map(lambda x: x == "1", value)))


class DayTimelineField(models.Charfield):
    """Поле, обозначающее расписание в рамках одного дня"""
    description = "Поле, обозначающее расписание в рамках одного дня"
    initial = {
        "null": False,
        "default": DayTimeline(),
        "help_text": "Обозначьте часы, в которые вы заняты",
        "max_length": 24
    }

    def __init__(self, *args, **kwargs):
        kwargs.update(self.initial)
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value: DayTimeline) -> str:
        return str(value)

    def from_db_value(self, value: str, expression, connection) -> str:
        return DayTimeline.parse_timeline(value)

    def to_python(self, value: Union[DayTimeline, str]) -> DayTimeline:
        if isinstance(value, DayTimeline):
            return value
        return DayTimeline.parse_timeline(value)
