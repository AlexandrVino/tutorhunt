from django.contrib.auth.models import UserManager

from core.managers import BaseManager


class HometaskManager(BaseManager, UserManager):
    pass
