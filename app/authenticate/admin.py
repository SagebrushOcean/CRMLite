from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'is_company_owner', 'is_superuser')
    list_display_links = ('id', 'email')
