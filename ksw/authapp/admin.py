from django.contrib import admin
from .models import WriterUser


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'last_login',
                    'is_active', 'is_staff', 'is_superuser')


admin.site.register(WriterUser, UserAdmin)
