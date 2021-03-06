from django.contrib.auth.models import UserManager
from django.db.models import QuerySet

from core.managers import BaseManager


class AppUserManager(BaseManager, UserManager):
    """Менеджер модели пользователя"""
    def get_users_with_role(self, role) -> QuerySet:
        return self.get_objects_with_filter(role=role)
