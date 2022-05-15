from django.contrib.auth import login

from users.models import User


class EmailUniqueFailed(BaseException):
    def __str__(self):
        return "Пользователь с этой почтой уже есть"


class EmailAuthBackend:
    @staticmethod
    def authenticate(request, email=None, password=None, user=None):
        try:
            print(locals())
            if user is None:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    return user
                return None
            else:
                login(request, user)
                return user
        except User.DoesNotExist:
            return None

    @staticmethod
    def create_user(email=None, username=None, password1=None, password2=None, **kwargs):
        """Create a new user profile"""

        if not email:
            raise ValueError("User must have an email address")

        if User.objects.filter(email=email):
            raise EmailUniqueFailed()

        user = User(email=email, username=username, **kwargs)
        user.set_password(password1)
        user.is_active = False
        user.save()

        return user

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
