from django.contrib.auth.models import UserManager

from core.managers import BaseManager


class HometaskManager(BaseManager, UserManager):
    pass


class AssignmentManager(BaseManager, UserManager):
    def get_students(self, *args, **kwargs):
        users = self.get_objects_with_filter(**kwargs)
        return users