from core.managers import BaseManager


class FollowManager(BaseManager):
    """Класс менеджера подписок"""
    def get_followers(self, follows=None, *args, **kwargs):
        if follows is None:
            follows = self.get_objects_with_filter(**kwargs, active=True)

        return follows.select_related("user_from").only(*args)
