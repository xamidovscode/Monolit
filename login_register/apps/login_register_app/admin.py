from django.contrib import admin
from .models import User


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email')
    list_display_links = ('id', 'first_name', 'last_name', 'email')
