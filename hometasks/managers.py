from core.managers import BaseManager


class HometaskManager(BaseManager):
    def get_teachers(self, *args, **kwargs):
        return self.get_objects_with_filter(**kwargs).select_related("teacher").only(*args)


class AssignmentManager(BaseManager):
    def get_students(self, *args, **kwargs):
        return self.get_objects_with_filter(**kwargs).select_related("student")
