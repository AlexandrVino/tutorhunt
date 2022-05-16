from django.contrib.auth.models import UserManager

from core.managers import BaseManager


class RatingManager(BaseManager, UserManager):
    def get_rating(self, *args, **kwargs):
        rating = self.get_objects_with_filter(**kwargs)
        return rating
