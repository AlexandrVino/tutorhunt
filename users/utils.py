from users.models import Bunch, User


def edit_user_data(user: User, **kwargs) -> None:
    for key, value in kwargs.items():
        if value is not None:
            user.__setattr__(key, value)
    user.save()


def update_user_timeline(user: User, day: int, time: int, value: bool):
    if user.has_timeline():
        user.timeline.get_days_fields()[day].set_hour(time, value)
        user.timeline.save()


def add_busy_hours(user: User, bunch: Bunch, value: bool):
    if bunch:
        day, time = map(int, bunch.datetime.split(":"))
        update_user_timeline(user, day - 1, time, value)
