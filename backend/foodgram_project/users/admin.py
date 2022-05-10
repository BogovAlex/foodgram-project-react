from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import User

admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email',
        'is_staff', 'is_superuser',
    )
    list_filter = ('email', 'username',)
    search_fields = ('email', 'username',)
