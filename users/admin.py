from django.contrib import admin
from users.models import Follow, Role, User, Bunch


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email',
        'is_active', 'date_joined', 'role', 'photo_tmb'
    )
    list_editable = ('is_active',)
    list_display_links = ('username',)

    fieldsets = ((None, {
        'fields': (
            'username', 'email', 'first_name', 'last_name', 'role', 'photo',
            'is_staff', 'is_active', 'user_permissions', 'date_joined',
        )
    }),)


@admin.register(Bunch)
class BunchAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'student', 'status')
    fieldsets = ((None, {'fields': ('teacher', 'student', 'status')}),)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "teacher":
            kwargs["queryset"] = User.manager.get_users_with_role(role=Role.TEACHER)
        elif db_field.name == "student":
            kwargs["queryset"] = User.manager.get_users_with_role(role=Role.STUDENT)

        return super(BunchAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user_from', 'user_to')
    fieldsets = ((None, {'fields': ('user_from', 'user_to')}),)
