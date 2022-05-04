from typing import Any, Dict, Iterable, List, Tuple, Union
from django.db import models



class DayTimeline:
    """Расписание дня"""
    timeline: List[bool]

    def __init__(self, timeline: Tuple[bool, ...] = None):
        if timeline is None:
            timeline = (False, ) * 24

        if not isinstance(timeline, tuple):
            raise TypeError("timeline должен быть кортежем")

        if len(timeline) != 24:
            raise ValueError("Количество часов должно быть равно 24")

        if any(map(lambda x: not isinstance(x, bool), timeline)):
            raise TypeError("В timeline могут быть только bool")

        self.timeline = timeline

    def __str__(self) -> str:
        return "".join(map(lambda x: "1" if x else "0", self.timeline))

    def __repr__(self) -> str:
        return str(self)

    def __len__(self):
        return 24

    def deconstruct(self) -> Tuple[str, Iterable[str], Dict[str, Any]]:
        """Функция деконструкции для сериализации"""
        name, args, kwargs = (
            "graphics.fields.DayTimeline", 
            (),
            {"timeline": self.timeline}
        ) 

        return name, args, kwargs

    def get_form_initial(self) -> List[str]:
        """Возвращает initial для DayTimelineFormField (список номеров часов)"""
        busy_hours = list(
            map(
                lambda x: x[0] + 1, # выдаёт номер часа
                filter(lambda x: x[1], enumerate(self.timeline))
            )
        )
        return busy_hours

    @classmethod
    def parse_timeline(cls, value: str) -> "DayTimeline":
        """
        Обработка строкового представления расписания. 
        
        Параметры:
        value -- строковое представление

        Возвращет соответствующий DayTimeline
        """
        return DayTimeline(timeline=tuple(map(lambda x: x == "1", value)))


    @classmethod
    def parse_formfield(cls, busy_hours: List[str]):
        """
        Обработка значений с формы.

        Параметры:
        busy_hours -- список с занятыми часами (получается с DayTimelineFormField)

        Возвращает соответствующий DayTimeline
        """
        timeline = [False] * 24
        for hour in busy_hours:
            timeline[int(hour) - 1] = True

        return DayTimeline(timeline=tuple(timeline))


class DayTimelineField(models.CharField):
    """Поле, обозначающее расписание в рамках одного дня"""
    from .formfields import DayTimelineFormField
    
    description = "Поле, обозначающее расписание в рамках одного дня"
    initial = {
        "null": False,
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

    def formfield(self, **kwargs):
        defaults = {
            "form_class": self.DayTimelineFormField,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
