from django.contrib import admin

from public_apps.company.models import Company, CompanyAddresses


class CompanyAddressesAdminInline(admin.StackedInline):
    model = CompanyAddresses
    extra = 0


class CompanyAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "owner", "created_at", "updated_at"]
    inlines = [
        CompanyAddressesAdminInline,
    ]


class CompanyAddressesAdmin(admin.ModelAdmin):
    list_display = ["id", "company", "country", "city", "address_line", "zip"]


admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyAddresses, CompanyAddressesAdmin)
