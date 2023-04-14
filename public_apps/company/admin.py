from django.contrib import admin

from public_apps.company.models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "owner", "created_at", "updated_at"]


admin.site.register(Company, CompanyAdmin)
