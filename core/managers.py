from django.db import models
from django.db.models import QuerySet


class BaseManager(models.Manager):
    """
    Дефолтный класс менеджера моделий
    """

    def get_objects(self) -> QuerySet:
        """
        :return: Возвращает все подписки
        """

        return self.all()

    def get_objects_list(self) -> list:
        """
        :return: возвращает все подписки (список)
        """

        return list(self.all())

    def get_objects_with_filter(self, *args, **kwargs) -> QuerySet:
        """
        :param args: картеж возвращаемых полей
        :param kwargs: словарь фильтров
        :return: отфильтрованые подписки
        """

        return self.filter(**kwargs).only(*args)

    def get_objects_with_filter_list(self, *args, **kwargs) -> list:
        """
        :param args: картеж возвращаемых полей
        :param kwargs: словарь фильтров
        :return: отфильтрованые подписки (список)
        """

        return list(self.filter(*args, **kwargs))
