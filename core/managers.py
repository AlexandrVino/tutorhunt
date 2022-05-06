from django.db import models
from django.db.models import QuerySet


class BaseManager(models.Manager):
    def get_objects(self) -> QuerySet:
        return self.all()

    def get_objects_list(self) -> list:
        return list(self.all())

    def get_objects_with_filter(self, *args, **kwargs) -> QuerySet:
        return self.filter(*args, **kwargs)

    def get_objects_with_filter_list(self, *args, **kwargs) -> list:
        return list(self.filter(*args, **kwargs))
