from django.contrib.auth import get_user_model
from django.db.models import Prefetch

from core.managers import BaseManager

User = get_user_model()


class ChatRoomManager(BaseManager):
    def join_owners(self, *args, **kwargs):
        return self.get_objects_with_filter(*args, **kwargs).select_related("first_user").select_related("second_user")


class MessagesManager(BaseManager):
    def join_owners(self, *args, **kwargs):
        return self.get_objects_with_filter(*args, **kwargs).order_by("-id").select_related("owner")[:30:-1]
