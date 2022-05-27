from django.contrib import admin

from follow.form_validations import follow_form_validation
from follow.models import Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("user_from", "user_to")
    fieldsets = ((None, {"fields": ("user_from", "user_to")}),)

    def get_form(self, request, obj=None, change=False, **kwargs):
        """
        Метод получения формы в админке
        Параметры:
            request: запрос
            obj:
            change:
            kwargs:
        """
        form = super(FollowAdmin, self).get_form(
            request, obj=None, change=False, **kwargs
        )
        form.is_valid = follow_form_validation
        return form
