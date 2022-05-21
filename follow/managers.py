from django.contrib.auth.models import UserManager

from core.managers import BaseManager


class FollowManager(BaseManager, UserManager):
    def get_followers(self, follows=None, *args, **kwargs):
        if follows is None:
            follows = self.get_objects_with_filter(**kwargs, active=True)

        return follows.select_related("user_from").only(*args)
