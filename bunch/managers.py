from django.contrib.auth import get_user_model

from core.managers import BaseManager

User = get_user_model()


class BunchManager(BaseManager):
    """Класс менеджера для связей, пока что просто заглушка"""
    def get_teacher_students(self, teacher: User, *args, **kwargs):
        return (
            self.get_objects_with_filter(teacher=teacher, **kwargs)
            .select_related("student").only(*args)
        )
