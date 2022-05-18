from django.contrib.auth import get_user_model
from django.db.models import Prefetch

from core.managers import BaseManager

User = get_user_model()


class ChatRoomManager(BaseManager):
    pass


class MessagesManager(BaseManager):
    def join_owners(self, *args, **kwargs):
        return self.get_objects_with_filter(*args, **kwargs).order_by("-id").select_related("owner")[:30:-1]
