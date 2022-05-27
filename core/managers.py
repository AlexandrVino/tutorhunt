from django.db import models
from django.db.models import QuerySet


class BaseManager(models.Manager):
    """Дефолтный класс менеджера моделей"""
    def get_objects(self) -> QuerySet:
        """Возвращает все объекты"""
        return self.all()

    def get_objects_list(self) -> list:
        """Возвращает все объекты (список)"""
        return list(self.all())

    def get_objects_with_filter(self, *args, **kwargs) -> QuerySet:
        """
        Параметры:
            args: кортеж возвращаемых полей
            kwargs: словарь фильтров
        Возвращает отфильтрованые объекты
        """
        return self.filter(**kwargs).only(*args)

    def get_objects_with_filter_list(self, *args, **kwargs) -> list:
        """
        Параметры:
            args: кортеж возвращаемых полей
            kwargs: словарь фильтров
        Возвращает отфильтрованые подписки (список)
        """
        return list(self.filter(*args, **kwargs))
