# # -*- coding: utf-8 -*-
from django.contrib import admin

from user_app.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "role", "is_active", "is_admin")
    list_filter = ("is_active", "is_admin")
    search_fields = ("username", "role")
