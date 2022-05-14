from users.models import User


def edit_user_data(user: User, **kwargs) -> None:
    print(kwargs)
    for key, value in kwargs.items():
        if value is not None:
            user.__setattr__(key, value)
    user.save()
