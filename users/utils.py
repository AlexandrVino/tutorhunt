from django.contrib.auth import get_user_model
from bunch.models import Bunch

User = get_user_model()


def edit_user_data(user: User, **kwargs) -> None:
    """
    :param user: User экземпляр модели пользователя
    :param kwargs: словарь измененных полей
    :return: None
    """

    for key, value in kwargs.items():
        if value is not None:
            user.__setattr__(key, value)
    user.save()


def update_user_timeline(user: User, day: int, time: int, value: bool) -> None:
    """
    :param user: User экземпляр модели пользователя
    :param day: int число от 1 до 7, номер дня недели
    :param time: int число от 0 до 23, номер часа в сутках
    :param value: освоболился или стал занятым час в графике
    :return: None
    """

    if user.has_timeline():
        user.timeline.get_days_fields()[day].set_hour(time, value)
        user.timeline.save()


def add_busy_hours(user: User, bunch: Bunch, value: bool) -> None:
    """
    :param user: User экземпляр модели пользователя
    :param bunch: Bunch экземпляр модели связи (занятия)
    :param value: освоболился или стал занятым час в графике
    :return: None
    """

    if bunch:
        day, time = map(int, bunch.datetime.split(":"))
        update_user_timeline(user, day - 1, time, value)
