from core.managers import BaseManager


class HometaskManager(BaseManager):
    pass


class AssignmentManager(BaseManager):
    def get_students(self, *args, **kwargs):
        return self.get_objects_with_filter(**kwargs)
