from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email', 'is_staff',
        'is_active', 'date_joined', 'role', 'photo'
    )
    list_editable = ('is_active',)
    list_display_links = ('username',)

    fieldsets = ((None, {
        'fields': (
            'username', 'email', 'first_name', 'last_name', 'role', 'photo',
            'is_staff', 'is_active', 'user_permissions', 'date_joined',
        )
    }),)
