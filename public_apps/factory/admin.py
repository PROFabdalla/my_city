from django.contrib import admin
from public_apps.factory.models import Factory


class FactoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "owner", "company"]


admin.site.register(Factory, FactoryAdmin)
