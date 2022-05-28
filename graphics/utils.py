from typing import Any, Dict, Iterable, List, Tuple


class CONST:
    WEEKDAYS = (
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday"
    )
    WEEKDAYS_RUS = (
        "понедельник",
        "вторник",
        "среда",
        "четверг",
        "пятница",
        "суббота",
        "воскресенье"
    )
    WEEKDAYS_RUS_CHOICES: Tuple[int, str] = tuple([
        (i + 1, weekday.capitalize())
        for i, weekday in enumerate(WEEKDAYS_RUS)
    ])
    """Выборы дня недели для форм"""
    HOURS = tuple(["%02d:00" % i for i in range(24)])


class DayTimeline:
    """Расписание дня"""
    timeline: List[bool]

    def __init__(self, timeline: Iterable[bool] = None):
        if timeline is None:
            timeline = [False for _ in range(24)]
        elif not hasattr(timeline, "__iter__"):
            raise TypeError("timeline должен быть итерируемым")
        elif not isinstance(timeline, list):
            timeline = list(timeline)

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

    def set_hour(self, hour: int, value: bool) -> None:
        """Меняет час (номер от 0 до 23) на value (True - занято, False - свободно)"""
        if not isinstance(value, bool):
            raise TypeError("value должно быть bool")
        self.timeline[hour] = value

    def is_busy(self, hour: int) -> bool:
        """Возвращает True, если час занят (часы от 0 до 23)"""
        return self.timeline[hour]

    def get_form_initial(self) -> List[str]:
        """Возвращает initial для DayTimelineFormField (список номеров занятых часов)"""
        busy_hours = []
        for i in range(24):
            if self.is_busy(i):
                busy_hours.append(i)
        return busy_hours

    @staticmethod
    def parse_timeline(value: str) -> "DayTimeline":
        """
        Обработка строкового представления расписания.
        Параметры:
            value: строковое представление
        Исключения:
            TypeError: если value не строка
        Возвращет соответствующий DayTimeline
        """
        if value:
            return DayTimeline(timeline=tuple(map(lambda x: x == "1", value)))
        elif isinstance(value, str):
            return DayTimeline()
        else:
            raise TypeError("value должно быть строкой")

    @staticmethod
    def parse_formfield(busy_hours: List[str]):
        """
        Обработка значений с формы.
        Параметры:
            busy_hours: список с занятыми часами (получается с DayTimelineFormField)
        Возвращает соответствующий DayTimeline
        """
        timeline = [False] * 24
        for hour in busy_hours:
            timeline[int(hour)] = True

        return DayTimeline(timeline=tuple(timeline))
