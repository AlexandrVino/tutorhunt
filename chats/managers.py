from django.contrib.auth import get_user_model
from core.managers import BaseManager

User = get_user_model()


class ChatRoomManager(BaseManager):
    """
    Класс менеджера для комнаты чата
    """

    def join_owners(self, *args, **kwargs):
        return self.get_objects_with_filter(**kwargs).select_related("first_user").select_related("second_user").only(
            *[f"first_user__{arg}" for arg in args], *[f"second_user__{arg}" for arg in args]
        )


class MessagesManager(BaseManager):
    """
    Класс менеджера для сообщений
    """

    def join_owners(self, *args, **kwargs):
        return self.get_objects_with_filter(*args, **kwargs).order_by("-id").select_related("owner").only(*args)[:30:-1]
