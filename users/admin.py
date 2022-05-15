from django.contrib import admin

from users.form_validations import bunch_form_validation, follow_form_validation
from users.models import Bunch, Follow, Role, User


def my_form_validation(form):
    data = form.__dict__.get("data")
    if data.get("user_from") == data.get("user_to"):
        form.add_error("user_to", "Пользователь не может быть подписан сам на себя")
    return form.is_bound and not form.errors


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "date_joined",
        "role",
        "photo_tmb",
    )
    list_editable = ("is_active",)
    list_display_links = ("username",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "role",
                    "photo",
                    "is_staff",
                    "is_active",
                    "user_permissions",
                    "date_joined",
                    "password",
                )
            },
        ),
    )


@admin.register(Bunch)
class BunchAdmin(admin.ModelAdmin):
    list_display = ("teacher", "student", "status")
    fieldsets = ((None, {"fields": ("teacher", "student", "status")}),)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "teacher":
            kwargs["queryset"] = User.manager.get_users_with_role(role=Role.TEACHER)
        elif db_field.name == "student":
            kwargs["queryset"] = User.manager.get_users_with_role(role=Role.STUDENT)

        return super(BunchAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(BunchAdmin, self).get_form(request, obj=None, change=False, **kwargs)
        form.is_valid = bunch_form_validation
        return form


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("user_from", "user_to")
    fieldsets = ((None, {"fields": ("user_from", "user_to")}),)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(FollowAdmin, self).get_form(
            request, obj=None, change=False, **kwargs
        )
        form.is_valid = my_form_validation
        return form
