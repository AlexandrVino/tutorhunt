from django.contrib.auth.models import UserManager
from django.db.models import QuerySet

from core.managers import BaseManager


class HometaskManager(BaseManager, UserManager):
    pass
