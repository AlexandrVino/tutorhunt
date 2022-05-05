from django.contrib.auth.models import UserManager
from django.db.models import QuerySet

from core.managers import BaseManager


class AppUserManager(BaseManager, UserManager):
    def get_users_with_role(self, role) -> QuerySet:
        return self.get_objects_with_filter(role=role)


class BunchManager(BaseManager, UserManager):
    pass


class FollowManager(BaseManager, UserManager):
    def get_followers(self, follows=None, *args, **kwargs):
        if follows is None:
            follows = self.get_objects_with_filter(**kwargs, active=True)

        return follows.select_related("user_from").only(*args)
