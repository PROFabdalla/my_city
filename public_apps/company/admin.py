from django.contrib import admin

from public_apps.company.models import Company, CompanyAddresses
from public_apps.employee.models import Employee


class CompanyAddressesAdminInline(admin.StackedInline):
    model = CompanyAddresses
    extra = 0


class EmployeeAdminInline(admin.StackedInline):
    model = Employee
    extra = 0


class CompanyAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "owner", "created_at", "updated_at"]
    inlines = [CompanyAddressesAdminInline, EmployeeAdminInline]


class CompanyAddressesAdmin(admin.ModelAdmin):
    list_display = ["id", "company", "country", "city", "address_line", "zip"]


admin.site.register(Company, CompanyAdmin)
admin.site.register(CompanyAddresses, CompanyAddressesAdmin)
