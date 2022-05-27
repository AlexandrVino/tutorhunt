from django.contrib import admin
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from bunch.form_validations import bunch_form_validation
from bunch.models import Bunch
from users.models import Role

User = get_user_model()


@admin.register(Bunch)
class BunchAdmin(admin.ModelAdmin):
    list_display = ("teacher", "student", "status", "datetime")
    fieldsets = ((None, {"fields": ("teacher", "student", "status", "datetime")}),)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Функция, изменяющая набор сущностей для полей модели Bunch
        Параметры:
            db_field: имя поля
            request: запрос
            kwargs: словарь контекста
        """
        if db_field.name == "teacher":
            kwargs["queryset"] = User.manager.get_users_with_role(role=Role.TEACHER)
        elif db_field.name == "student":
            kwargs["queryset"] = User.manager.get_users_with_role(role=Role.STUDENT)

        return super(BunchAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, change=False, **kwargs) -> ModelForm:
        """
        Функция перехвата создания формы с целью изменить функцию валидации
        Параметры
            request: запрос
            obj:
            change:
            kwargs: словарь контекста
        Возвращает форму
        """
        form = super(BunchAdmin, self).get_form(request, obj=obj, change=change, **kwargs)
        form.is_valid = bunch_form_validation
        return form
