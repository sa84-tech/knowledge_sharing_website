from django.contrib import admin
from .models import WriterUser


class UserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'username', 'last_login',
                    'is_active', 'is_staff', 'is_superuser')


admin.site.register(WriterUser, UserAdmin)
