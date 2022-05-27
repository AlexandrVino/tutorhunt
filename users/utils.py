from django.contrib.auth import get_user_model
from bunch.models import Bunch

User = get_user_model()


def edit_user_data(user: User, **kwargs) -> None:
    """
    Параметры:
        user: экземпляр модели пользователя
        kwargs: словарь измененных полей
    """
    for key, value in kwargs.items():
        if value is not None:
            if key == "bio":
                value = value.lower()
            user.__setattr__(key, value)
    user.save()


def update_user_timeline(user: User, day: int, time: int, value: bool) -> None:
    """
    Параметры:
        user: экземпляр модели пользователя
        day: число от 1 до 7, номер дня недели
        time: число от 0 до 23, номер часа в сутках
        value: освоболился или стал занятым час в графике
    """
    if user.has_timeline():
        user.timeline.get_days_fields()[day].set_hour(time, value)
        user.timeline.save()


def add_busy_hours(user: User, bunch: Bunch, value: bool) -> None:
    """
    Параметры:
        user: экземпляр модели пользователя
        bunch: экземпляр модели связи (занятия)
        value: освоболился или стал занятым час в графике
    """
    if bunch:
        day, time = map(int, bunch.datetime.split(":"))
        update_user_timeline(user, day - 1, time, value)
