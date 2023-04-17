from django.contrib import admin

from public_apps.employee.models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "company",
    )


admin.site.register(Employee, EmployeeAdmin)
