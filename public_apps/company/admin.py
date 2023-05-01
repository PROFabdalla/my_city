from django.contrib import admin

from public_apps.company.models import Company
from public_apps.addresses.models import Addresses
from public_apps.employee.models import Employee


class CompanyAddressesAdminInline(admin.StackedInline):
    model = Addresses
    extra = 0


class EmployeeAdminInline(admin.StackedInline):
    model = Employee
    extra = 0


class CompanyAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "owner", "created_at", "updated_at"]
    inlines = [CompanyAddressesAdminInline, EmployeeAdminInline]


admin.site.register(Company, CompanyAdmin)
